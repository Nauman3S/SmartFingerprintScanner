String serverName;
String channelId;
String userKey;
String timezone = "";
String apiKey;
String apid;
String hostName = "SmartJ";
String minActiveValue = "0";
String ampSensorType;
String sensorSelection;
String apPass;
String settingsPass;
String Photosensor = "0";
String tempUnits = "";

#if defined(ARDUINO_ARCH_ESP8266)
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#elif defined(ARDUINO_ARCH_ESP32)
#include <WiFi.h>
#include <WebServer.h>
#endif

#include <ESPmDNS.h>
#include "SoftwareStack.h"
#ifndef BUILTIN_LED
#define BUILTIN_LED 2 // backward compatibility
#endif
#if defined(ARDUINO_ARCH_ESP8266)
#ifdef AUTOCONNECT_USE_SPIFFS
FS &FlashFS = SPIFFS;
#else
#include <LittleFS.h>
FS &FlashFS = LittleFS;
#endif
#elif defined(ARDUINO_ARCH_ESP32)
#include <SPIFFS.h>
fs::SPIFFSFS &FlashFS = SPIFFS;
#endif
#include "statusLED.h"
#include "neo_timer.h"

#define GET_CHIPID() ((uint16_t)(ESP.getEfuseMac() >> 32))

unsigned long lastPub = 0;
unsigned int updateInterval = 2000;


SoftwareStack ss; // SS instance
String loggedIn = "";

String mac = (WiFi.macAddress());
char __mac[sizeof(mac)];

const char *mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char *mqtt_user = "testUser";
const char *mqtt_pass = "testUser@123";
const char *mqtt_client_name = __mac; //"12312312312332212";// any random alphanumeric stirng
//////////////////////////////
#define BUFFER_SIZE 250
String incoming = "";
String incomingTopic = "";
WiFiClient wclient;


String LastUpdated = "";
String internetStatus = "Not-Connected";
int selectedDeviceIndex = 0;
String connectionMode = "WiFi";

int wifi_connect_tries=0;
int connectToWiFi(String ssid, String password) {
  Serial.println("Connecting to WiFi...");

  WiFi.begin(ssid.c_str(), password.c_str());

  while (WiFi.status() != WL_CONNECTED) {
    if(wifi_connect_tries>=10){
      return 0;//error
    }
    delay(1000);
    wifi_connect_tries++;
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Connected to WiFi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  return 1;//connected
}