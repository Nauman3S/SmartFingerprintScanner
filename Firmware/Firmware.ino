#include "consts.h"
#include "button_handler.h"
#include "actuatorHandler.h"
#include "headers.h" //all misc. headers and functions
#include "esp32InternalTime.h"
#include "MQTTFuncs.h" //MQTT related functions
#include "webApp.h"    //Captive Portal webpages
#include <FS.h>        //ESP32 File System

const long interval = 1000 * 60 * 5;        // Interval at which to read sensors//5 mintues
Neotimer dataAcqTimer = Neotimer(interval); // Set timer's preset
Neotimer sensorsDataTimer = Neotimer(1000); // Set timer's preset

IPAddress ipV(192, 168, 4, 1);
String loadParams(AutoConnectAux &aux, PageArgument &args) // function to load saved settings
{
    (void)(args);
    File param = FlashFS.open(PARAM_FILE, "r");
    String v1 = "0";
    String v2 = "0";
    String v3 = "0";
    String v4 = "0";
    String v5 = "0";
    String v6 = "0";
    String v7 = "0";
    String v8 = "0";

    if (param)
    {
        Serial.println("load params func");
        aux.loadElement(param);
        Serial.println(param);
        // Serial.println(args);

        AutoConnectText &BTN1ValueElm = aux["BTN1"].as<AutoConnectText>();
        AutoConnectText &BTN2ValueElm = aux["BTN2"].as<AutoConnectText>();
        AutoConnectText &BTN3ValueElm = aux["BTN3"].as<AutoConnectText>();
        AutoConnectText &BTN4ValueElm = aux["BTN4"].as<AutoConnectText>();
        AutoConnectText &BTN5ValueElm = aux["BTN5"].as<AutoConnectText>();
        AutoConnectText &BTN6ValueElm = aux["BTN6"].as<AutoConnectText>();
        // vibSValueElm.value="VibS:91122";#

        v1 = String(BTN1ValueElm.value);
        v2 = String(BTN2ValueElm.value);
        v3 = String(BTN3ValueElm.value);
        v4 = String(BTN4ValueElm.value);
        v5 = String(BTN5ValueElm.value);
        v6 = String(BTN6ValueElm.value);

        if (v1.length() > 0)
        {
        }

        BTN1ValueElm.value = String("Button 1: ") + getButtonState(BTN_1);
        BTN2ValueElm.value = String("Button 2: ") + getButtonState(BTN_2);
        BTN3ValueElm.value = String("Button 3: ") + getButtonState(BTN_3);
        BTN4ValueElm.value = String("Button 4: ") + getButtonState(BTN_4);
        BTN5ValueElm.value = String("Button 5: ") + getButtonState(BTN_5);
        BTN6ValueElm.value = String("Button 6: ") + getButtonState(BTN_6);

        // curSValueElm.value="CurS:7788";
        param.close();
    }
    else
        Serial.println(PARAM_FILE " open failed");
    return String("");
}

String saveParams(AutoConnectAux &aux, PageArgument &args) // save the settings
{
    serverName = args.arg("mqttserver"); // broker
    serverName.trim();

    channelId = args.arg("channelid");
    channelId.trim();

    userKey = args.arg("userkey"); // user name
    userKey.trim();

    apiKey = args.arg("apikey"); // password
    apiKey.trim();

    timezone = args.arg("timezone"); // timezone
    timezone.trim();

    apPass = args.arg("apPass"); // ap pass
    apPass.trim();

    settingsPass = args.arg("settingsPass"); // ap pass
    settingsPass.trim();

    hostName = args.arg("hostname");
    hostName.trim();

    // The entered value is owned by AutoConnectAux of /mqtt_setting.
    // To retrieve the elements of /mqtt_setting, it is necessary to get
    // the AutoConnectAux object of /mqtt_setting.
    File param = FlashFS.open(PARAM_FILE, "w");
    portal.aux("/mqtt_setting")->saveElement(param, {"mqttserver", "channelid", "userkey", "apikey", "timezone", "hostname", "apPass", "settingsPass"});
    param.close();

    // Echo back saved parameters to AutoConnectAux page.
    AutoConnectText &echo = aux["parameters"].as<AutoConnectText>();
    echo.value = "Server: " + serverName + "<br>";
    echo.value += "Channel ID: " + channelId + "<br>";
    echo.value += "Timezone: " + timezone + "<br>";
    echo.value += "Username: " + userKey + "<br>";
    echo.value += "Password: " + apiKey + "<br>";
    echo.value += "ESP host name: " + hostName + "<br>";
    echo.value += "AP Password: " + apPass + "<br>";
    echo.value += "Settings Page Password: " + settingsPass + "<br>";
    mqttPublish("SmartJ/dev/config", String("tz;") + timezone); // publish timezone info
    return String("");
}
bool loadAux(const String auxName) // load defaults from data/*.json
{
    bool rc = false;
    Serial.println("load aux func");
    String fn = auxName + ".json";
    File fs = FlashFS.open(fn.c_str(), "r");
    if (fs)
    {
        rc = portal.load(fs);
        fs.close();
    }
    else
        Serial.println("Filesystem open failed: " + fn);
    return rc;
}
uint8_t inAP = 0;
bool whileCP()
{

    if (inAP == 0)
    {
        ledState(AP_MODE);
        inAP = 1;
    }
    // Serial.println("AP MODE");

    loopLEDHandler();
}

void setup() // main setup functions
{
    Serial.begin(115200);
    delay(1000);
    setupButtons();
    setupActuator();

    if (!MDNS.begin("smartj")) // starting mdns so that user can access webpage using url `esp32.local`(will not work on all devices)
    {
        Serial.println("Error setting up MDNS responder!");
        while (1)
        {
            delay(1000);
        }
    }
#if defined(ARDUINO_ARCH_ESP8266)
    FlashFS.begin();
#elif defined(ARDUINO_ARCH_ESP32)
    FlashFS.begin(true);
#endif
    loadAux(AUX_MQTTSETTING);
    loadAux(AUX_MQTTSAVE);
    AutoConnectAux *setting = portal.aux(AUX_MQTTSETTING);
    if (setting) // get all the settings parameters from setting page on esp32 boot
    {
        Serial.println("Setting loaded");
        PageArgument args;
        AutoConnectAux &mqtt_setting = *setting;
        loadParams(mqtt_setting, args);
        AutoConnectInput &hostnameElm = mqtt_setting["hostname"].as<AutoConnectInput>();
        AutoConnectInput &apPassElm = mqtt_setting["apPass"].as<AutoConnectInput>();
        AutoConnectInput &serverNameElm = mqtt_setting["mqttserver"].as<AutoConnectInput>();
        AutoConnectInput &channelidElm = mqtt_setting["channelid"].as<AutoConnectInput>();
        AutoConnectInput &userkeyElm = mqtt_setting["userkey"].as<AutoConnectInput>();
        AutoConnectInput &apikeyElm = mqtt_setting["apikey"].as<AutoConnectInput>();
        AutoConnectInput &settingsPassElm = mqtt_setting["settingsPass"].as<AutoConnectInput>();
        // vibSValueElm.value="VibS:11";
        serverName = String(serverNameElm.value);
        channelId = String(channelidElm.value);
        userKey = String(userkeyElm.value);
        apiKey = String(apikeyElm.value);
        hostName = String(hostnameElm.value);
        apPass = String(apPassElm.value);
        settingsPass = String(settingsPassElm.value);
        if (hostnameElm.value.length())
        {
            // hostName=hostName+ String("-") + String(GET_CHIPID(), HEX);
            //;
            // portal.config(hostName.c_str(), apPass.c_str());
            //  portal.config(hostName.c_str(), "123456789AP");
            config.apid = hostName; // hostnameElm.value+ "-" + String(GET_CHIPID(), HEX);
            config.password = apPass;
            config.psk = apPass;
            // portal.config(hostName.c_str(), "123456789AP");
            Serial.println("(from hostELM) hostname set to " + hostName);
        }
        else
        {

            // hostName = String("OEE");;
            // portal.config(hostName.c_str(), "123456789AP");
            config.apid = hostName; // hostnameElm.value+ "-" + String(GET_CHIPID(), HEX);
            config.password = apPass;
            config.psk = apPass;
            // config.hostName = hostName;//hostnameElm.value+ "-" + String(GET_CHIPID(), HEX);
            //  portal.config(hostName.c_str(), "123456789AP");
            Serial.println("hostname set to " + hostName);
        }
        config.homeUri = "/_ac";
        config.apip = ipV;

        portal.on(AUX_MQTTSETTING, loadParams);
        portal.on(AUX_MQTTSAVE, saveParams);
    }
    else
    {
        Serial.println("aux. load error");
    }
    // config.homeUri = "/_ac";
    config.apip = ipV;
    config.autoReconnect = true;
    config.reconnectInterval = 1;
    Serial.print("AP: ");
    Serial.println(hostName);
    Serial.print("Password: ");
    Serial.println(apPass);
    config.title = "Smart Joystick"; // set title of webapp

    // add different tabs on homepage
    portal.append("/api-now", "api-now");
    portal.append("/api", "api");
    portal.append("/LiveSensors", "LiveSensors");
    portal.append("/data", "DataTable");
    portal.disableMenu(AC_MENUITEM_DISCONNECT);
    server.on("/", handleRoot);
    server.on("/api-now", cmotsValues);
    server.on("/api", api);
    server.on("/LiveSensors", live);
    server.on("/data", dataTable);
    // Starts user web site included the AutoConnect portal.

    config.auth = AC_AUTH_DIGEST;
    config.authScope = AC_AUTHSCOPE_PARTIAL;
    config.username = hostName;
    config.password = settingsPass;

    portal.config(config);
    portal.whileCaptivePortal(whileCP);
    portal.onDetect(atDetect);
    portal.load(FPSTR(PAGE_AUTH));
    if (portal.begin())
    {
        Serial.println("Started, IP:" + WiFi.localIP().toString());
        ledState(AP_MODE);
    }
    else
    {
        Serial.println("Connection failed.");
        while (true)
        {
            yield();
            delay(100);
        }
    }

    MDNS.addService("http", "tcp", 80);
    mqttConnect(); // start mqtt
}
String latestValues = "";
void loop()
{
    server.handleClient();
    portal.handleRequest();
    loopLEDHandler();

    if (millis() - lastPub > updateInterval) // publish data to mqtt server
    {
        latestValues =
            getButtonState(BTN_1) + String(";") + getButtonState(BTN_2) + String(";") + getButtonState(BTN_3) + String(";") +
            getButtonState(BTN_4) String(";") + getButtonState(BTN_5) + String(";") + getButtonState(BTN_6);
        mqttPublish("smartj/" + String(hostName), getTimestamp() + String(";") + latestValues); // publish data to mqtt broker
        Serial.println(latestValues);

        ledState(ACTIVE_MODE);

        lastPub = millis();
    }
    if (!mqttClient.connected())
    {
        reconnect();
    }
    mqttClient.loop();
    if (WiFi.status() == WL_IDLE_STATUS)
    {
        ledState(IDLE_MODE);
        ESP.restart();

        delay(1000);
    }
}