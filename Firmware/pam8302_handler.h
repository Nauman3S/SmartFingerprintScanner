// AudioPlayer.h

#ifndef AUDIO_PLAYER_H
#define AUDIO_PLAYER_H

#include <Arduino.h>
#include <AudioFileSourceSPIFFS.h>
#include <AudioGeneratorMP3.h>
#include <AudioOutputI2S.h>

class AudioPlayer
{
private:
    AudioGeneratorMP3 *mp3;
    AudioFileSourceSPIFFS *file;
    AudioOutputI2S *out;
    uint8_t currentFile = 0;
    const int SD_PIN = 14; // Shutdown pin connected to GPIO14

public:
    AudioPlayer()
    {
        mp3 = nullptr;
        file = nullptr;
        out = nullptr;
    }

    void setup_audio()
    {
        // Initialize SPIFFS
        if (!SPIFFS.begin())
        {
            Serial.println("Failed to mount SPIFFS");
            return;
        }
        out = new AudioOutputI2S(0, 1); // 0 = DAC_CHANNEL_1 (GPIO25), 1 = DAC_CHANNEL_2 (GPIO26)

        // Initialize the SD pin
        pinMode(SD_PIN, OUTPUT);
        digitalWrite(SD_PIN, HIGH); // Enable the amplifier by default
    }

    void loop_audio()
    {
        if (mp3 && mp3->isRunning())
        {
            if (!mp3->loop())
            {
                mp3->stop();
                delete mp3;
                delete file;
                mp3 = nullptr;
                file = nullptr;
            }
        }
    }

    void play_audio(uint8_t file_number)
    {
        if (file_number == currentFile)
            return; // If the same file is already playing, do nothing

        if (mp3 && mp3->isRunning())
        {
            mp3->stop();
            delete mp3;
            delete file;
        }

        if (file_number == 1)
        {
            file = new AudioFileSourceSPIFFS("/welcome.mp3");
        }
        else if (file_number == 2)
        {
            file = new AudioFileSourceSPIFFS("/goodbye.mp3");
        }
        else
        {
            Serial.println("Invalid file number");
            return;
        }

        mp3 = new AudioGeneratorMP3();
        mp3->begin(file, out);
        currentFile = file_number;
    }

    // Function to enable the amplifier
    void enableAmp()
    {
        digitalWrite(SD_PIN, HIGH);
    }

    // Function to disable the amplifier
    void disableAmp()
    {
        digitalWrite(SD_PIN, LOW);
    }
};

#endif // AUDIO_PLAYER_H
