#ifndef IR_SENSOR_H
#define IR_SENSOR_H

#include <Arduino.h>

const char IRLeft         = 7;
const char IRMiddleLeft   = 6;
const char IRMiddle       = 5;
const char IRMiddleRight  = 4;
const char IRRight        = 3;

class IRSensor
{
    public:
        static void Init();
        static boolean ReadLeft();
        static boolean ReadMiddleLeft();
        static boolean ReadMiddle();
        static boolean ReadMiddleRight();
        static boolean ReadRight();
};

#endif