#ifndef DC_MOTORS_H
#define DC_MOTORS_H

#include <Arduino.h>

const int RightMotorA   = 13;
const int RightMotorB   = 12;
const int LeftMotorA    = 9;
const int LeftMotorB    = 8;
const int LeftMotorPWM  = 11;
const int RigthMotorPWM = 10;

class DcMotors
{
    public:
        static void Init();
        //dir = true means front direction
        static void ActivateLeftMotor(int pwm, boolean dir);
        static void ActivateRightMotor(int pwm, boolean dir);
};

#endif
