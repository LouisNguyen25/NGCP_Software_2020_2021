#include <SoftwareSerial.h>

const int xInput = A0;
const int yInput = A1;
const int zInput = A2;
const int buttonPin = 2;

// Make sure these two variables are correct for your setup
int scale = 200; // 3 (±3g) for ADXL337, 200 (±200g) for ADXL377
boolean micro_is_5V = false; // Set to true if using a 5V microcontroller such as the Arduino Uno, false if using a 3.3V microcontroller, this affects the interpretation of the sensor data

// Raw Ranges:
// initialize to mid-range and allow calibration to
// find the minimum and maximum for each axis
int xRawMin = 0;
int xRawMax = 1024;

int yRawMin = 0;
int yRawMax = 1024;

int zRawMin = 0;
int zRawMax = 1024;

// Take multiple samples to reduce noise
const int sampleSize = 10;

void setup() 
{
 analogReference(EXTERNAL);
 Serial.begin(9600);
 
 AutoCalibrate(ReadAxis(xInput),ReadAxis(yInput),ReadAxis(zInput));

 Serial.print("X,");
 Serial.print("Y,");
 Serial.println("Z");
}

void loop() 
{
 int rawX = ReadAxis(xInput);
 int rawY = ReadAxis(yInput);
 int rawZ = ReadAxis(zInput);
 
 if (digitalRead(buttonPin) == LOW)
 {
   AutoCalibrate(rawX, rawY, rawZ);
 }

 else
 {
  //    Serial.print("Raw Ranges: X: ");
  //    Serial.print(xRawMin);
  //    Serial.print("-");
  //    Serial.print(xRawMax);
   
  //    Serial.print(", Y: ");
  //    Serial.print(yRawMin);
  //    Serial.print("-");
  //    Serial.print(yRawMax);
   
  //    Serial.print(", Z: ");
  //    Serial.print(zRawMin);
  //    Serial.print("-");
  //    Serial.print(zRawMax);
   
  //    Serial.println();
  //    Serial.print(xRaw);
  //    Serial.print(", ");
  //    Serial.print(yRaw);
  //    Serial.print(", ");
  //    Serial.print(zRaw);
   
  // Scale accelerometer ADC readings into common units
  // Scale map depends on if using a 5V or 3.3V microcontroller
  float scaledX, scaledY, scaledZ; // Scaled values for each axis
  if (micro_is_5V) // Microcontroller runs off 5V
  {
    scaledX = mapf(rawX, 0, 675, -scale, scale); // 3.3/5 * 1023 =~ 675
    scaledY = mapf(rawY, 0, 675, -scale, scale);
    scaledZ = mapf(rawZ, 0, 675, -scale, scale);
  }
  else // Microcontroller runs off 3.3V
  {
    scaledX = mapf(rawX, 0, 1023, -scale, scale);
    scaledY = mapf(rawY, 0, 1023, -scale, scale);
    scaledZ = mapf(rawZ, 0, 1023, -scale, scale);
  }
 
   Serial.print(scaledX);
   Serial.print(", ");
   Serial.print(scaledY);
   Serial.print(", ");
   Serial.print(scaledZ);
   Serial.println("");
 
   delay(50);
 }
}

int ReadAxis(int axisPin)
{
 long reading = 0;
 analogRead(axisPin);
 delay(1);
 for (int i = 0; i < sampleSize; i++)
 {
   reading += analogRead(axisPin);
 }
 return reading/sampleSize;
}

// Same functionality as Arduino's standard map function, except using floats
float mapf(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void AutoCalibrate(int xRaw, int yRaw, int zRaw)
{
 Serial.println("Calibrating...");
 if (xRaw < xRawMin)
 {
   xRawMin = xRaw;
 }
 if (xRaw > xRawMax)
 {
   xRawMax = xRaw;
 }
 
 if (yRaw < yRawMin)
 {
   yRawMin = yRaw;
 }
 if (yRaw > yRawMax)
 {
   yRawMax = yRaw;
 }

 if (zRaw < zRawMin)
 {
   zRawMin = zRaw;
 }
 if (zRaw > zRawMax)
 {
   zRawMax = zRaw;
 }
}

//#include <SD.h>
//#include <SPI.h>
//#define FILENAME "log.csv"
//
//const int buttonPin = 2;
//
//CSVFile csv;    
//SdFat sd;
////PrintFile output = createWriter(FILENAME);
//
//int scale = 200; // +/- 200g (ADXL377)
//boolean micro_is_5V = true; // what kinda microcontroller are we using? check voltage
//// ^Set to true if using a 5V microcontroller such as the Arduino Uno, false if using 
//// a 3.3V microcontroller, this affects the interpretation of the sensor data
//
//
//void initSdFile()
//{
// if (sd.exists(FILENAME) && !sd.remove(FILENAME))
// {
//   Serial.println("Failed init remove file");
//   return;
// }
// if (!csv.open(FILENAME, O_RDWR | O_CREAT)) {
//   Serial.println("Failed open file");
// }
//}
//
//void loop()
//{
//  // Get raw accelerometer data for each axis
//  int rawX = analogRead(A0);
//  int rawY = analogRead(A1);
//  int rawZ = analogRead(A2);
//
//  // initSdFile();
//
//  // csv.open(FILENAME);
//  //  csv.write(rawX);
//  //  csv.write(rawY);
//  //  csv.write(rawZ);
//  //  csv.write("\n");
//  //  csv.close();
//
//  // Scale accelerometer ADC readings into common units
//  // Scale map depends on if using a 5V or 3.3V microcontroller
//  float scaledX, scaledY, scaledZ; // Scaled values for each axis
//  if (micro_is_5V) // Microcontroller runs off 5V
//  {
//    scaledX = mapf(rawX, 0, 675, -scale, scale); // 3.3/5 * 1023 =~ 675
//    scaledY = mapf(rawY, 0, 675, -scale, scale);
//    scaledZ = mapf(rawZ, 0, 675, -scale, scale);
//  }
//  else // Microcontroller runs off 3.3V
//  {
//    scaledX = mapf(rawX, 0, 1023, -scale, scale);
//    scaledY = mapf(rawY, 0, 1023, -scale, scale);
//    scaledZ = mapf(rawZ, 0, 1023, -scale, scale);
//  }
//
//  // Print out raw X,Y,Z accelerometer readings
//  Serial.print("X: "); Serial.println(rawX);
//  Serial.print("Y: "); Serial.println(rawY);
//  Serial.print("Z: "); Serial.println(rawZ);
//  Serial.println();
//
//  // Print out scaled X,Y,Z accelerometer readings
//  Serial.print("X: "); Serial.print(scaledX); Serial.println(" g");
//  Serial.print("Y: "); Serial.print(scaledY); Serial.println(" g");
//  Serial.print("Z: "); Serial.print(scaledZ); Serial.println(" g");
//  Serial.println();
//
//  //saveData(scaledX,scaledY,scaledZ);
//
//  //output.Read
//
//  delay(2000); // Minimum delay of 2 milliseconds between sensor reads (500 Hz)
//  File csvFile = SD.open(FILENAME, FILE_WRITE);
//  if(csvFile)
//  {
//    csvFile.print("thisIsInColumnOneRowOne");
//    csvFile.print(",");
//    csvFile.println("thisIsInColumnTwoRowOne");
//
//    csvFile.print("thisIsInColumnOneRowTwo");
//    csvFile.print(",");
//    csvFile.println("thisIsInColumnTwoRowTwo");
//
//    csvFile.close();
//  } 
//}
//
//// Same functionality as Arduino's standard map function, except using floats
//float mapf(float x, float in_min, float in_max, float out_min, float out_max)
//{
//  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
//}
//

/*
_/﹋\_
(҂`_´)
<,︻╦╤─ ҉ - -  SAY HELLO TO MY LIL FRIEND!!!
_/﹋\_
*/
