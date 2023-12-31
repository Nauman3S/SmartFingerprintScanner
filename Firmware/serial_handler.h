
String incomingData;
bool newDataAvailable = false;

void serial_callback(String payload)
{
    // This function is called when new data arrives
    // Serial.println("Callback triggered with payload: " + payload);

    // For demonstration, let's send a response back
    //   serial_publish("Acknowledged: " + payload);
    if (payload.indexOf("network") >= 0)
    {
        String wifi_ssid = ss.StringSeparator(payload, ';', 1);
        String wifi_pass = ss.StringSeparator(payload, ';', 2);
        if (connectToWiFi(wifi_ssid, wifi_pass))
        {
            serial_publish("Connected to: " + wifi_ssid);
        }
        else
        {
            serial_publish("Can't connect to: " + wifi_ssid);
        }
    }
    else if (payload.indexOf("get_wifi") >= 0)
    {
        scanForNetworks(); // Get the list of SSIDs
        serial_publish("networks;" + networks);
    }
    else if (payload.indexOf("enroll") >= 0){
        enroll_fingerprint(1);
    }
}

void serial_publish(String payload)
{
    Serial.println(payload);
}

void serial_handler()
{
    if (Serial.available())
    {
        incomingData = Serial.readStringUntil('\n'); // Read the incoming data until newline
        newDataAvailable = true;
    }

    if (newDataAvailable)
    {
        serial_callback(incomingData);
        newDataAvailable = false;
    }
}