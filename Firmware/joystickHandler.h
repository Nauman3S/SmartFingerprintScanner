#include <Wire.h>
#include <Adafruit_ADS1X15.h>
Adafruit_ADS1115 ads;

int adc0, adc1, adc2, adc3;             // ADC Readings
int X1angle, Y1angle, X2angle, Y2angle; // Joystick Angle Variables

void setupADS1115()
{
    ads.begin();
}
uint16_t getADS1115Values(int type)
{
    adc0 = ads.readADC_SingleEnded(0);
    adc1 = ads.readADC_SingleEnded(1);
    adc2 = ads.readADC_SingleEnded(2);
    adc3 = ads.readADC_SingleEnded(3);
    if (type == J1_X_AXIX)
    {
        X1angle = map(adc2, 15, 23564, 0, 180);
        return X1angle;
    }
    else if (type == J1_Y_AXIX)
    {
        Y1angle = map(adc3, 1818, 23564, 0, 180);
        return Y1angle;
    }
    else if (type == J2_X_AXIX)
    {
        X2angle = map(adc0, 98, 23504, 0, 180);
        return X2angle;
    }
    else if (type == J2_Y_AXIX)
    {
        Y2angle = map(adc1, 19, 23510, 0, 180);
        return Y2angle;
    }
}