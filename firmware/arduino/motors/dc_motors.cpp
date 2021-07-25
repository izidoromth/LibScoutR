#include "dc_motors.h"

char NormalizePWM(char pwm)
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
void DcMotors::ActivateLeftMotor(char pwm, boolean dir)
{
    digitalWrite(LeftMotorA, dir ? LOW : HIGH);
    digitalWrite(LeftMotorB, dir ? HIGH : LOW);
    analogWrite(LeftMotorPWM, NormalizePWM(pwm));
}
void DcMotors::ActivateRightMotor(char pwm, boolean dir)
{
    digitalWrite(RightMotorA, dir ? LOW : HIGH);
    digitalWrite(RightMotorB, dir ? HIGH : LOW);
    analogWrite(RigthMotorPWM, NormalizePWM(pwm));
}