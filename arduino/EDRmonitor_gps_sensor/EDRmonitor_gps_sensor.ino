#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>

/*
 * GPSModule: read latitude, longitude, and altitude
 *  Pinout:
 *    - RXPin: Digital 3
 *    - TXPin: Digital 4
 *    - 3.3 - 5 V
 *    - GND
 */
static const int RXPin = 3, TXPin = 4;
static const uint32_t GPSBaud = 9600;
const int BUFFER_SIZE = JSON_OBJECT_SIZE(10);

// The TinyGPS++ object
TinyGPSPlus gps;

// The serial connection to the GPS device
SoftwareSerial softwareSerial(RXPin, TXPin);


void setup() {
  Serial.begin(9600);
  softwareSerial.begin(GPSBaud);
}


void loop() {
  StaticJsonDocument<BUFFER_SIZE> JSONencoder;
  
  // This sketch displays information every time a new sentence is correctly encoded.
  while (softwareSerial.available() > 0) {
    gps.encode(softwareSerial.read());
    if (gps.location.isUpdated()) {
      JSONencoder["latitude"] = gps.location.lat();
      JSONencoder["longitude"] = gps.location.lng();
      JSONencoder["altitude"] = gps.altitude.meters();
    }
  }

  // Convert Arduino json encoder into string.
  String output;
  serializeJson(JSONencoder, output);
  if(!JSONencoder.isNull())
    Serial.println(output);
}
