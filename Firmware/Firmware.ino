#include "consts.h"
#include "headers.h" //all misc. headers and functions
#include "esp32InternalTime.h"
#include <FS.h> //ESP32 File System
#include "serial_handler.h"

const long interval = 1000 * 60 * 5;        // Interval at which to read sensors//5 mintues
Neotimer dataAcqTimer = Neotimer(interval); // Set timer's preset
Neotimer sensorsDataTimer = Neotimer(1000); // Set timer's preset

IPAddress ipV(192, 168, 4, 1);

uint8_t inAP = 0;
String networks = "";
void scanForNetworks()
{
    int numberOfNetworks = WiFi.scanNetworks();

    // Dynamically allocate memory for the SSID array

    for (int i = 0; i < numberOfNetworks; i++)
    {
        networks = networks + WiFi.SSID(i) + ";"; // Store only the SSID
    }
}

void setup() // main setup functions
{
    Serial.begin(115200);
    delay(1000);
    scanForNetworks(); // Get the list of SSIDs
    
}
String latestValues = "";
void loop()
{

    loopLEDHandler();
    serial_handler();

    if (millis() - lastPub > updateInterval) // publish data to mqtt server
    {

        serial_publish("networks;"+networks);

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