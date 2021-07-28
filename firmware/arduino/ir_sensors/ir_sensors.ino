#include "ir_sensor.h"

void setup() {
  Serial.begin(9600);
  IRSensor::Init();
}

void loop() {
  delay(500);
  boolean U1 = IRSensor::ReadLeft();
  boolean U2 = IRSensor::ReadMiddleLeft();
  boolean U3 = IRSensor::ReadMiddle();
  boolean U4 = IRSensor::ReadMiddleRight();
  boolean U5 = IRSensor::ReadRight();
  Serial.println("U1: " + String(U1) + " | U2: " + String(U2) + " | U3: " + String(U3) + " | U4: " + String(U4) + " | U5: " + String(U5));
}
