#include "ir_sensor.h"

void IRSensor::Init()
{
    pinMode(IRLeft,        INPUT);
    pinMode(IRMiddleLeft,  INPUT);
    pinMode(IRMiddle,      INPUT);
    pinMode(IRMiddleRight, INPUT);
    pinMode(IRRight,       INPUT);
}
boolean IRSensor::ReadLeft()
{
    return digitalRead(IRLeft);
}
boolean IRSensor::ReadMiddleLeft()
{
    return digitalRead(IRMiddleLeft);
}
boolean IRSensor::ReadMiddle()
{
    return digitalRead(IRMiddle);
}
boolean IRSensor::ReadMiddleRight()
{
    return digitalRead(IRMiddleRight);
}
boolean IRSensor::ReadRight()
{
    return digitalRead(IRRight);
}