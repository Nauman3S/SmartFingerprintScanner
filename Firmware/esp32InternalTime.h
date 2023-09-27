
// RTC
#include <ESP32Time.h>
ESP32Time rtc;
void syncTime(String timestampPkt);
String getTimestamp();

// RTC_DATA_ATTR int bootCount = 0;

void syncTime(String timestampPkt)
{
    String rawNTP, dayStamp, timeStamp, temp;
    rawNTP = timestampPkt;
    // rawNTP = timeClient.getFormattedDate();
    int sc, min, hr, dy, mon, yr, mls;
    temp = ss.StringSeparator(rawNTP, ';', 0);
    sc = temp.toInt();
    temp = ss.StringSeparator(rawNTP, ';', 1);
    min = temp.toInt();
    temp = ss.StringSeparator(rawNTP, ';', 2);
    hr = temp.toInt();
    temp = ss.StringSeparator(rawNTP, ';', 3);
    dy = temp.toInt();
    temp = ss.StringSeparator(rawNTP, ';', 4);
    mon = temp.toInt();
    temp = ss.StringSeparator(rawNTP, ';', 5);
    yr = temp.toInt();
    temp = ss.StringSeparator(rawNTP, ';', 6);
    mls = temp.toInt();

    rtc.setTime(sc, min, hr, dy, mon, yr, mls);

    Serial.println("Synchronising DATE AND TIME:");
    dayStamp = rtc.getDate();
    timeStamp = rtc.getTime();
    Serial.print("Date: ");
    Serial.println(dayStamp);
    Serial.print("Time: ");
    Serial.println(timeStamp);
}

String getTimestamp()
{

    String ts = rtc.getTime("%A %B %d %Y %H:%M:%S");
    ts = ts + String(".") + String(rtc.getMillis());

    return ts;
}