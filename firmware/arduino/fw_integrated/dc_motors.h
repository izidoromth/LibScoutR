#ifndef DC_MOTORS_H
#define DC_MOTORS_H

#include <Arduino.h>

const int RightMotorA   = 9;
const int RightMotorB   = 8;
const int LeftMotorA    = 13;
const int LeftMotorB    = 12;
const int LeftMotorPWM  = 10;
const int RigthMotorPWM = 11;

class DcMotors
{
    public:
        static void Init();
        //dir = true means front direction
        static void ActivateLeftMotor(int pwm, boolean dir);
        static void ActivateRightMotor(int pwm, boolean dir);
};

#endif
