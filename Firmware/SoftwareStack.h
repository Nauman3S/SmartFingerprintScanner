// Software Stack

class SoftwareStack
{
public:
#define DebugPrint(x) Serial.println(x)

    String StringSeparator(String data, char separator, int index);
    char *StrToCharArray(String data);

    SoftwareStack();

private:
    char buf[100];

    int sensorVCounter = 0;
};
SoftwareStack::SoftwareStack()
{
}

char *SoftwareStack::StrToCharArray(String data)
{
    data.toCharArray(this->buf, data.length() + 1);
    return this->buf;
}

String SoftwareStack::StringSeparator(String data, char separator, int index)
{

    int found = 0;
    int strIndex[] = {0, -1};
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++)
    {
        if (data.charAt(i) == separator || i == maxIndex)
        {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i + 1 : i;
        }
    }

    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

String SoftwareStack::getMACAddress()
{
    String TrackerID = String(WiFi.macAddress());
    TrackerID = stringSeparator(TrackerID, ':', 0) + stringSeparator(TrackerID, ':', 1) + stringSeparator(TrackerID, ':', 2) + stringSeparator(TrackerID, ':', 3) +
                stringSeparator(TrackerID, ':', 4) + stringSeparator(TrackerID, ':', 5);
    return TrackerID;
}
String SoftwareStack::getTopicWithMAC(String before_mac, String after_mac)
{

    String t = before_mac + getMACAddress() + after_mac;

    return t;
}