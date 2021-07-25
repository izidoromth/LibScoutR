const int IN1 = 13;
const int IN2 = 12;
const int IN3 = 9;
const int IN4 = 8;
const int ENA = 11;
const int ENB = 10;
const int PWM = 100;

#include "dc_motors.h"

void setup() {
  Serial.begin(9600); // start serial port at 9600 bps:
  DcMotors::Init();
}
void loop()

{
//  digitalWrite(MotorPin, HIGH);
  if (Serial.available() > 0) {
    char serialread = Serial.read();
    switch(serialread){
      //forward direction
      case 'w':
        DcMotors::ActivateLeftMotor(PWM, true);
        DcMotors::ActivateRightMotor(PWM, true);
      break;
      //backward direction
      case 's':
        DcMotors::ActivateLeftMotor(PWM, false);
        DcMotors::ActivateRightMotor(PWM, false);
      break;
      //left direction
      case 'a':
        DcMotors::ActivateLeftMotor(PWM, false);
        DcMotors::ActivateRightMotor(PWM, true);
      break;
      //right direction
      case 'd':
        DcMotors::ActivateLeftMotor(PWM, true);
        DcMotors::ActivateRightMotor(PWM, false);
      break;
      //stop
      case 'e':
        DcMotors::ActivateLeftMotor(0, true);
        DcMotors::ActivateRightMotor(0, true);
      break;
    }
  }
//  if (Serial.available() > 0) {
//    char serialread = Serial.read();
//    switch(serialread){
//      //forward direction
//      case 'w':
//      Serial.print(serialread);
//      analogWrite(ENA, PWM);
//      analogWrite(ENB, PWM);
//      //control direction 
//      digitalWrite(IN1, HIGH);
//      digitalWrite(IN2, LOW);
//      digitalWrite(IN3, HIGH);
//      digitalWrite(IN4, LOW);
//      break;
//      //backward direction
//      case 's':
//      Serial.print(serialread);
//      analogWrite(ENA, PWM);
//      analogWrite(ENB, PWM);
//      //control direction 
//      digitalWrite(IN1, LOW);
//      digitalWrite(IN2, HIGH);
//      digitalWrite(IN3, LOW);
//      digitalWrite(IN4, HIGH);
//      break;
//      //left direction
//      case 'a':
//      Serial.print(serialread);
//      analogWrite(ENA, 0);
//      analogWrite(ENB, PWM);
//      //control direction 
//      digitalWrite(IN1, LOW);
//      digitalWrite(IN2, LOW);
//      digitalWrite(IN3, HIGH);
//      digitalWrite(IN4, LOW);
//      break;
//      //right direction
//      case 'd':
//      Serial.print(serialread);
//      analogWrite(ENA, PWM);
//      analogWrite(ENB, 0);
//      //control direction 
//      digitalWrite(IN1, HIGH);
//      digitalWrite(IN2, LOW);
//      digitalWrite(IN3, LOW);
//      digitalWrite(IN4, LOW);
//      break;
//      //stop
//      case 'e':
//      Serial.print(serialread);
//      analogWrite(ENA, 0);
//      analogWrite(ENB, 0);
//      break;
//      
//    }
    
// }
}

//int MotorPin = 4;      // MotorPin set to pin2
//int Motorforward = 5;   // MotorDirectionPin set to pin3
//int Motorbackward = 6;   // MotorDirectionPin set to pin3
//
//
//
//void setup()
//
//{
//  Serial.begin(9600); // start serial port at 9600 bps:
//  while (!Serial) {
//    ; // wait for serial port to connect. Needed for Leonardo only
//  }
//  pinMode(MotorPin, OUTPUT);  // sets the pin as output
//  pinMode(Motorforward, OUTPUT); // sets the pin as output
//  pinMode(Motorbackward, OUTPUT);
//  establishContact(); 
//}
//
//
//
//void loop()
//
//{
//  digitalWrite(MotorPin, HIGH);
//  
//  if (Serial.available() > 0) {
//    char serialread = Serial.read();
//    switch(serialread){
//      case 'w':
//      Serial.print(serialread);
//      analogWrite(Motorforward, 130);
//      analogWrite(Motorbackward, 0);
//      break;
//      case 's':
//      Serial.print(serialread);
//      analogWrite(Motorforward, 0);
//      analogWrite(Motorbackward, 130);
//      break;
//      case 'a':
//      Serial.print(serialread);
//      analogWrite(Motorforward, 0);
//      analogWrite(Motorbackward, 0);
//      break;
//      case 'e':
//      Serial.print(serialread);
//      analogWrite(Motorforward, 255);
//      analogWrite(Motorbackward, 0);
//      break;
//      case 'd':
//      Serial.print(serialread);
//      analogWrite(Motorforward, 0);
//      analogWrite(Motorbackward, 255);
//      break;
//      
//    }
//    
//  }
//}
//
//void establishContact() {
//  while (Serial.available() <= 0) {
//    Serial.print('A');   // send a capital A
//    delay(300);
//  }
//} 
