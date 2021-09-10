/*
  SD card read/write

  This example shows how to read and write data to and from an SD card file
  The circuit:
   SD card attached to SPI bus as follows:
 ** MOSI - pin 11
 ** MISO - pin 12
 ** CLK - pin 13
 ** CS - pin 4 (for MKRZero SD: SDCARD_SS_PIN)

  created   Nov 2010
  by David A. Mellis
  modified 9 Apr 2012
  by Tom Igoe

  This example code is in the public domain.

*/

#include <SoftwareSerial.h>
#include <SPI.h>
#include <SD.h>

const int xInput = A0;
const int yInput = A1;
const int zInput = A2;
const int buttonPin = 2;

// Make sure these two variables are correct for your setup
int scale = 200; // 3 (±3g) for ADXL337, 200 (±200g) for ADXL377
boolean micro_is_5V = false; // Set to true if using a 5V microcontroller such as the Arduino Uno, false if using a 3.3V microcontroller, this affects the interpretation of the sensor data

File myFile;

// Raw Ranges:
// initialize to mid-range and allow calibration to
// find the minimum and maximum for each axis
int xRawMin = 512;
int xRawMax = 512;

int yRawMin = 512;
int yRawMax = 512;

int zRawMin = 512;
int zRawMax = 512;

int xRaw = analogRead(xInput);
int yRaw = analogRead(yInput);
int zRaw = analogRead(zInput);

// Take multiple samples to reduce noise
const int sampleSize = 10;
void setup() 
{
    // Open serial communications and wait for port to open:
    analogReference(EXTERNAL);
    Serial.begin(9600);
    while (!Serial) 
    {
        ; // Wait for serial port to connect. Needed for native USB port only
    }

    Serial.print("Initializing SD card...");

    if (!SD.begin(10)) 
    {
        Serial.println("initialization failed!");
        while (1);
    }
    Serial.println("initialization done.");

    // Open the file. note that only one file can be open at a time,
    // so you have to close this one before opening another.
    myFile = SD.open("test.csv", FILE_WRITE);
    //AutoCalibrate(ReadAxis(xInput),ReadAxis(yInput),ReadAxis(zInput));
    AutoCalibrate();
    myFile.print("X,");
    myFile.print("Y,");
    myFile.println("Z");
    myFile.close();
//   // if the file opened okay, write to it:
//     if (myFile) {
//     Serial.print("Writing to test.csv...");
//     myFile.println("testing 1, 2, 3.");
//     // close the file:
//     myFile.close();
//     Serial.println("done.");
//     } else {
//     // if the file didn't open, print an error:
//     Serial.println("error opening test.csv");
//     }

//   // re-open the file for reading:
//     myFile = SD.open("test.csv");
//     if (myFile) {
//         Serial.println("test.csv:");

//         // read from the file until there's nothing else in it:
//         while (myFile.available()) {
//             Serial.write(myFile.read());
//         }
//         // close the file:
//         myFile.close();
//         } else {
//     // if the file didn't open, print an error:
//     Serial.println("error opening test.csv");
//   }

}

void loop() {

    myFile = SD.open("test.csv", FILE_WRITE);
    // int xRaw = ReadAxis(xInput);
    // int yRaw = ReadAxis(yInput);
    // int zRaw = ReadAxis(zInput);
 
    xRaw = analogRead(xInput);
    yRaw = analogRead(yInput);
    zRaw = analogRead(zInput);
    while (digitalRead(buttonPin) == LOW)
    {
        // AutoCalibrate(xRaw, yRaw, zRaw);
        AutoCalibrate();
    }
    
        // Convert raw values to 'milli-Gs"
        // long scaledX = map(xRaw, xRawMin, xRawMax, -1000, 1000);
        // long scaledY = map(yRaw, yRawMin, yRawMax, -1000, 1000);
        // long scaledZ = map(zRaw, zRawMin, zRawMax, -1000, 1000);
  
        // // re-scale to fractional Gs
        // float xAccel = scaledX / 1000.0;
        // float yAccel = scaledY / 1000.0;
        // float zAccel = scaledZ / 1000.0;

        // Scale accelerometer ADC readings into common units
        // Scale map depends on if using a 5V or 3.3V microcontroller

        // float scaledX, scaledY, scaledZ; // Scaled values for each axis
        // if (micro_is_5V) // Microcontroller runs off 5V
        // {
        //     scaledX = mapf(xRaw, 0, 675, -scale, scale); // 3.3/5 * 1023 =~ 675
        //     scaledY = mapf(yRaw, 0, 675, -scale, scale);
        //     scaledZ = mapf(zRaw, 0, 675, -scale, scale);
        // }
        // else // Microcontroller runs off 3.3V
        // {
        //     scaledX = mapf(xRaw, 0, 1023, -scale, scale);
        //     scaledY = mapf(yRaw, 0, 1023, -scale, scale);
        //     scaledZ = mapf(zRaw, 0, 1023, -scale, scale);
        // }


    myFile.print(xRaw);
    myFile.print(", ");
    myFile.print(yRaw);
    myFile.print(", ");
    myFile.print(zRaw);
    myFile.println("");
    myFile.close();
    
    
   

}

int ReadAxis(int axisPin)
{
    long reading = 0;
    analogRead(axisPin);
    delay(0.1);
    for (int i = 0; i < sampleSize; i++)
    {
        reading += analogRead(axisPin);
    }
    return reading/sampleSize;
}

// Same functionality as Arduino's standard map function, except using floats
float mapf(float x, float in_min, float in_max, float out_min, float out_max)   //512,0,1023,-200,200
{
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void AutoCalibrate()
{
    myFile.println("Calibrating...");
    xRaw = 512;
    yRaw = 512;
    zRaw = 512;
}

// void AutoCalibrate(int xRaw, int yRaw, int zRaw)
// {
//     myFile.println("Calibrating...");
//     if (xRaw < xRawMin)
//     {
//         xRawMin = xRaw;
//     }
//     if (xRaw > xRawMax)
//     {
//         xRawMax = xRaw;
//     }
 
//     if (yRaw < yRawMin)
//     {
//         yRawMin = yRaw;
//     }
//     if (yRaw > yRawMax)
//     {
//         yRawMax = yRaw;
//     }

//     if (zRaw < zRawMin)
//     {
//         zRawMin = zRaw;
//     }
//     if (zRaw > zRawMax)
//     {
//         zRawMax = zRaw;
//     }
// }

/*
_/﹋\_
(҂`_´)
<,︻╦╤─ ҉ - -  SAY HELLO TO MY LIL FRIEND!!!
_/﹋\_
*/

