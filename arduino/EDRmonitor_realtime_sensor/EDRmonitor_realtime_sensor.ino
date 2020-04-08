#include <ArduinoJson.h>


float mapfloat(long x, long in_min, long in_max, long out_min, long out_max){
  return (float)(x - in_min) * (out_max - out_min) / (float)(in_max - in_min) + out_min;
}

/*
 * RotarySpeed: Read the speed from rotary encoder (LPD3806)
 *  Pinout:
 *    - D2: Interrupt Pin 0
 *    - D3: Interrupt Pin 1
 *    - 5V
 *    - GND
 */
class RotarySpeed{
  public:
    long _interval = 1000;
    unsigned long _lastTime = 0;
    volatile unsigned long _counter = 0;
    int INTPIN = 2;

  boolean isInterval() {
    unsigned long currentTime = millis();
    if (currentTime - _lastTime >= _interval) {
      _lastTime = _lastTime + _interval;
      return true;
    } 
    else if (currentTime < _lastTime)
      _lastTime = 0;
    else
      return false;
  }
  
  void resetCounter() {
    _counter = 0;
  }
  
  float pprToSpeed(){
    return mapfloat(_counter, 0, 400, 0, 100);
  }
};


/*
 * PedalPercent: Read value from the pedal
 *  Pinout:
 *    - A0: Analog Pin
 *    - 5V
 *    - GND
 */
class PedalPercent{
  public:
    int PEDALPIN = A0;

  int read(){
    int val = analogRead(PEDALPIN);
    return map(val, 0, 1023, 0, 100);
  }
};



RotarySpeed rotarySpeed = RotarySpeed();
PedalPercent pedalPercent = PedalPercent();
const int BUFFER_SIZE = JSON_OBJECT_SIZE(10);


void setup() {
  // Begin serial communication
  Serial.begin(9600);

  // Start pinMode of
  // - Rotary: speed -> [0, Inf)
  // - Pedal: percentage -> [0, 1023]
  pinMode(rotarySpeed.INTPIN, INPUT);
  pinMode(pedalPercent.PEDALPIN, INPUT);

  // Attach Interrupt rotary pin (D2) to update rotary speed
  attachInterrupt(0, updateCounter, RISING);
  digitalWrite(rotarySpeed.INTPIN, HIGH);
}

void loop() {
  /*
   * Main loop function:
   *  1). Read rotary and pedal sensors.
   *  2). Preprocess the values of these two.
   *  3). Encoder them into the json format.
   *  4). Serial to String format.
   */
  StaticJsonDocument<BUFFER_SIZE> JSONencoder;
  JSONencoder["speed"] = rotarySpeed.pprToSpeed();
  JSONencoder["pedal"] = pedalPercent.read();

  String output;
  serializeJson(JSONencoder, output);
  Serial.println(output);
  
  if(rotarySpeed.isInterval())
    rotarySpeed.resetCounter();
}


void updateCounter(){
  rotarySpeed._counter++;
}
