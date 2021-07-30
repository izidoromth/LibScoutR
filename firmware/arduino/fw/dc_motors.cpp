#include "dc_motors.h"

char NormalizePWM(int pwm)
{
    return (pwm < 0) ? 0 : (pwm > 255) ? 255 : pwm;
}
void DcMotors::Init()
{
    pinMode(LeftMotorA, OUTPUT);
    pinMode(LeftMotorB, OUTPUT);
    pinMode(RightMotorA, OUTPUT);
    pinMode(RightMotorB, OUTPUT);
}
void DcMotors::ActivateLeftMotor(int pwm, boolean dir)
{
    digitalWrite(LeftMotorA, dir ? LOW : HIGH);
    digitalWrite(LeftMotorB, dir ? HIGH : LOW);
    analogWrite(LeftMotorPWM, NormalizePWM(pwm));
}
void DcMotors::ActivateRightMotor(int pwm, boolean dir)
{
    digitalWrite(RightMotorA, dir ? LOW : HIGH);
    digitalWrite(RightMotorB, dir ? HIGH : LOW);
    analogWrite(RigthMotorPWM, NormalizePWM(pwm));
}
