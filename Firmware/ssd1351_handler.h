void setup_ssd1351();
void initScreen();
void updateText1(String text);
void updateText2(String text);
void drawFSJpeg(const char *filename, int xpos, int ypos);
void jpegRender(int xpos, int ypos);
void jpegInfo();
void createArray(const char *filename);

#include "SPIFFS.h"
#include <JPEGDecoder.h>

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1351.h>
#include <Adafruit_Sensor.h>

uint32_t delayMS;

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 128

#define SCLK_PIN 18
#define MOSI_PIN 23
#define DC_PIN   4
#define CS_PIN   5
#define RST_PIN  19

// Color definitions
#define BLACK 0x0000
#define BLUE 0x001F
#define RED 0xF800
#define GREEN 0x07E0
#define CYAN 0x07FF
#define MAGENTA 0xF81F
#define YELLOW 0xFFE0
#define WHITE 0xFFFF

const String fileLogo = "/logo.jpg";
const String fileImage = "/image.jpg";

Adafruit_SSD1351 tft = Adafruit_SSD1351(SCREEN_WIDTH, SCREEN_HEIGHT, CS_PIN, DC_PIN, MOSI_PIN, SCLK_PIN, RST_PIN);

String prev_text1;
String prev_text2;

void setup_ssd1351()
{
    // Initialize device.

    tft.begin();
    tft.fillRect(0, 0, 128, 128, WHITE);

    if (!SPIFFS.begin())
    {
        while (1)
            yield();
    }

    initScreen();
    updateText1("Welcome");
    updateText2("FingerprintScan");
}

void initScreen()
{
    drawFSJpeg(fileLogo.c_str(), 0, 0);
    drawFSJpeg(fileImage.c_str(), 0, 64);

    tft.setCursor(72, 24);
    tft.setTextColor(BLACK);
    tft.setTextSize(3);
    tft.print("?");

    tft.setCursor(72, 88);
    tft.setTextColor(BLACK);
    tft.setTextSize(3);
    tft.print("?");
}

void updateText1(String text)
{
    if (prev_text1 != text)
    {
        tft.fillRect(64, 0, 128, 64, WHITE);
        tft.setCursor(70, 24);
        tft.setTextColor(BLACK);
        tft.setTextSize(3);
        String tempString = "";
        tempString += text;
        tempString += ".";
        tft.print(tempString);
        prev_text1 = text;
    }
}

void updateText2(String text)
{
    if (prev_text2 != text)
    {
        tft.fillRect(64, 64, 128, 128, WHITE);
        tft.setCursor(70, 88);
        tft.setTextColor(BLACK);
        tft.setTextSize(3);
        String tempString = "";
        tempString += text;
        tempString += ".";
        tft.print(tempString);
        prev_text2 = text;
    }
}

/*====================================================================================
  Support functions to render the Jpeg images.
  ==================================================================================*/

// Return the minimum of two values a and b
#define minimum(a, b) (((a) < (b)) ? (a) : (b))

//====================================================================================
//   This function opens the Filing System Jpeg image file and primes the decoder
//====================================================================================
void drawFSJpeg(const char *filename, int xpos, int ypos)
{

    Serial.println("=====================================");
    Serial.print("Drawing file: ");
    Serial.println(filename);
    Serial.println("=====================================");

    // Open the file (the Jpeg decoder library will close it)
    fs::File jpgFile = SPIFFS.open(filename, "r"); // File handle reference for SPIFFS
    //  File jpgFile = SD.open( filename, FILE_READ);  // or, file handle reference for SD library

    if (!jpgFile)
    {
        Serial.print("ERROR: File \"");
        Serial.print(filename);
        Serial.println("\" not found!");
        return;
    }

    // To initialise the decoder and provide the file, we can use one of the three following methods:
    // boolean decoded = JpegDec.decodeFsFile(jpgFile); // We can pass the SPIFFS file handle to the decoder,
    // boolean decoded = JpegDec.decodeSdFile(jpgFile); // or we can pass the SD file handle to the decoder,
    boolean decoded = JpegDec.decodeFsFile(filename); // or we can pass the filename (leading / distinguishes SPIFFS files)
                                                      // The filename can be a String or character array
    if (decoded)
    {
        // print information about the image to the serial port
        jpegInfo();

        // render the image onto the screen at given coordinates
        jpegRender(xpos, ypos);
    }
    else
    {
        Serial.println("Jpeg file format not supported!");
    }
}

//====================================================================================
//   Decode and paint onto the TFT screen
//====================================================================================
void jpegRender(int xpos, int ypos)
{

    // retrieve infomration about the image
    uint16_t *pImg;
    uint16_t mcu_w = JpegDec.MCUWidth;
    uint16_t mcu_h = JpegDec.MCUHeight;
    uint32_t max_x = JpegDec.width;
    uint32_t max_y = JpegDec.height;

    // Jpeg images are draw as a set of image block (tiles) called Minimum Coding Units (MCUs)
    // Typically these MCUs are 16x16 pixel blocks
    // Determine the width and height of the right and bottom edge image blocks
    uint32_t min_w = minimum(mcu_w, max_x % mcu_w);
    uint32_t min_h = minimum(mcu_h, max_y % mcu_h);

    // save the current image block size
    uint32_t win_w = mcu_w;
    uint32_t win_h = mcu_h;

    // record the current time so we can measure how long it takes to draw an image
    uint32_t drawTime = millis();

    // save the coordinate of the right and bottom edges to assist image cropping
    // to the screen size
    max_x += xpos;
    max_y += ypos;

    // read each MCU block until there are no more
    while (JpegDec.read())
    {

        // save a pointer to the image block
        pImg = JpegDec.pImage;

        // calculate where the image block should be drawn on the screen
        int mcu_x = JpegDec.MCUx * mcu_w + xpos;
        int mcu_y = JpegDec.MCUy * mcu_h + ypos;

        // check if the image block size needs to be changed for the right edge
        if (mcu_x + mcu_w <= max_x)
            win_w = mcu_w;
        else
            win_w = min_w;

        // check if the image block size needs to be changed for the bottom edge
        if (mcu_y + mcu_h <= max_y)
            win_h = mcu_h;
        else
            win_h = min_h;

        // copy pixels into a contiguous block
        if (win_w != mcu_w)
        {
            for (int h = 1; h < win_h - 1; h++)
            {
                memcpy(pImg + h * win_w, pImg + (h + 1) * mcu_w, win_w << 1);
            }
        }

        // draw image MCU block only if it will fit on the screen
        if ((mcu_x + win_w) <= tft.width() && (mcu_y + win_h) <= tft.height())
        {
            tft.drawRGBBitmap(mcu_x, mcu_y, pImg, win_w, win_h);
        }

        // Stop drawing blocks if the bottom of the screen has been reached,
        // the abort function will close the file
        else if ((mcu_y + win_h) >= tft.height())
            JpegDec.abort();
    }

    // calculate how long it took to draw the image
    drawTime = millis() - drawTime;

    // print the results to the serial port
    Serial.print("Total render time was    : ");
    Serial.print(drawTime);
    Serial.println(" ms");
    Serial.println("=====================================");
}

//====================================================================================
//   Send time taken to Serial port
//====================================================================================
void jpegInfo()
{
    Serial.println(F("==============="));
    Serial.println(F("JPEG image info"));
    Serial.println(F("==============="));
    Serial.print(F("Width      :"));
    Serial.println(JpegDec.width);
    Serial.print(F("Height     :"));
    Serial.println(JpegDec.height);
    Serial.print(F("Components :"));
    Serial.println(JpegDec.comps);
    Serial.print(F("MCU / row  :"));
    Serial.println(JpegDec.MCUSPerRow);
    Serial.print(F("MCU / col  :"));
    Serial.println(JpegDec.MCUSPerCol);
    Serial.print(F("Scan type  :"));
    Serial.println(JpegDec.scanType);
    Serial.print(F("MCU width  :"));
    Serial.println(JpegDec.MCUWidth);
    Serial.print(F("MCU height :"));
    Serial.println(JpegDec.MCUHeight);
    Serial.println(F("==============="));
}

//====================================================================================
//   Open a Jpeg file and dump it to the Serial port as a C array
//====================================================================================
void createArray(const char *filename)
{

    fs::File jpgFile; // File handle reference for SPIFFS
    //  File jpgFile;  // File handle reference For SD library

    if (!(jpgFile = SPIFFS.open(filename, "r")))
    {
        Serial.println(F("JPEG file not found"));
        return;
    }

    uint8_t data;
    byte line_len = 0;
    Serial.println("// Generated by a JPEGDecoder library example sketch:");
    Serial.println("// https://github.com/Bodmer/JPEGDecoder");
    Serial.println("");
    Serial.println("#if defined(__AVR__)");
    Serial.println("  #include <avr/pgmspace.h>");
    Serial.println("#endif");
    Serial.println("");
    Serial.print("const uint8_t ");
    while (*filename != '.')
        Serial.print(*filename++);
    Serial.println("[] PROGMEM = {"); // PROGMEM added for AVR processors, it is ignored by Due

    while (jpgFile.available())
    {

        data = jpgFile.read();
        Serial.print("0x");
        if (abs(data) < 16)
            Serial.print("0");
        Serial.print(data, HEX);
        Serial.print(","); // Add value and comma
        line_len++;
        if (line_len >= 32)
        {
            line_len = 0;
            Serial.println();
        }
    }

    Serial.println("};\r\n");
    // jpgFile.seek( 0, SeekEnd);
    jpgFile.close();
}
//====================================================================================