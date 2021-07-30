#include "dc_motors.h"

const int PWM = 100; 

void setup() {
  Serial.begin(9600); // start serial port at 9600 bps:
  DcMotors::Init();
}
void loop()
{
  if(Serial.available() > 0)
  {
    char serialread = Serial.read();
    if(serialread == 'w')
    {
      DcMotors::ActivateLeftMotor(PWM, true);
      DcMotors::ActivateRightMotor(PWM, true);

      delay(2000);

      DcMotors::ActivateLeftMotor(0, true);
      DcMotors::ActivateRightMotor(0, true);
    }
  }
}
//void loop()
//{
////  digitalWrite(MotorPin, HIGH);
//  if (Serial.available() > 0) {
//    char serialread = Serial.read();
//    switch(serialread){
//      //forward direction
//      case 'w':
//        DcMotors::ActivateLeftMotor(PWM, true);
//        DcMotors::ActivateRightMotor(PWM, true);
//      break;
//      //backward direction
//      case 's':
//        DcMotors::ActivateLeftMotor(PWM, false);
//        DcMotors::ActivateRightMotor(PWM, false);
//      break;
//      //left direction
//      case 'a':
//        DcMotors::ActivateLeftMotor(PWM, false);
//        DcMotors::ActivateRightMotor(PWM, true);
//      break;
//      //right direction
//      case 'd':
//        DcMotors::ActivateLeftMotor(PWM, true);
//        DcMotors::ActivateRightMotor(PWM, false);
//      break;
//      //stop
//      case 'e':
//        DcMotors::ActivateLeftMotor(0, true);
//        DcMotors::ActivateRightMotor(0, true);
//      break;
//    }
//  }
