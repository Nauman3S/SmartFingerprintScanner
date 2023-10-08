#include "consts.h"
#include "headers.h" //all misc. headers and functions
#include "esp32InternalTime.h"
#include <FS.h> //ESP32 File System
#include "fingerprint_handler.h"
#include "serial_handler.h"
#include "ssd1351_handler.h"
#include "pam8302_handler.h"

const long interval = 1000 * 60 * 5;        // Interval at which to read sensors//5 mintues
Neotimer dataAcqTimer = Neotimer(interval); // Set timer's preset
Neotimer sensorsDataTimer = Neotimer(1000); // Set timer's preset

IPAddress ipV(192, 168, 4, 1);

uint8_t wifi_connect_try = 0;

AudioPlayer audioPlayer;

void setup() // main setup functions
{
    Serial.begin(115200);
    setup_ssd1351();
    audioPlayer.setup_audio();
    audioPlayer.play_audio(1);

    delay(1000);
    setup_ssd1351();
    delay(500);
    scanForNetworks(); // Get the list of SSIDs
    setup_fingerprint_sensor();

    while (1)
    {
        wifi_connect_tries++;

        if (wifi_connect_tries >= 8 && WiFi.status() != WL_CONNECTED)
        {
            Serial.println("Can't connect to WiFi");
            break;
        }
        if (wifi_connect_tries >= 8 && WiFi.status() == WL_CONNECTED)
        {
            Serial.println("Connected to WiFi!");
            break;
        }
    }
}
String latestValues = "";
void loop()
{

    loopLEDHandler();
    serial_handler();
    audioPlayer.loop_audio();

    if (millis() - lastPub > updateInterval) // publish data to mqtt server
    {

        ledState(ACTIVE_MODE);

        lastPub = millis();
    }

    if (WiFi.status() == WL_IDLE_STATUS)
    {
        ledState(IDLE_MODE);
        // ESP.restart();

        delay(1000);
    }
}