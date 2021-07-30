#include "dc_motors.h"
#include "ir_sensor.h"

#define RightInitialSpeed 100
#define LeftInitialSpeed 100

float Kp = 1;
float Ki = 1;
float Kd = 1;

int Sensor[] = {A1, A2, A3, A4, A5};
float P = 0;
float I = 0;
float D = 0;
int Error = 0;

int Previous_Error, Previous_I;
int PID_value;
int Left_Speed, Right_Speed;

void setup()
{
    Serial.begin(9600);
    DcMotors::Init();
    IRSensor::Init();

    DcMotors::ActivateLeftMotor(200, true);
    DcMotors::ActivateRightMotor(200, true);
    delay(100);
}

void loop() 
{
    CalculateError();
    Calculate_PID();
    MotorControl();
}
                                                                                                                                                                 
void CalculateError()
{
    boolean left = !IRSensor::ReadLeft();
    boolean m_left = !IRSensor::ReadMiddleLeft();
    boolean middle = !IRSensor::ReadMiddle();
    boolean m_right = !IRSensor::ReadMiddleRight();
    boolean right = !IRSensor::ReadRight();
    
    //Serial.println("U1: " + String(left) + " | U2: " + String(m_left) + " | U3: " + String(middle) + " | U4: " + String(m_right) + " | U5: " + String(right));

    if((left == 1) && (m_left == 0) && (middle == 0) && (m_right == 0) && (right == 0))
        Error = 4;
    else if((left == 1) && (m_left == 1) && (middle == 0) && (m_right == 0) && (right == 0))
        Error = 3;
    else if((left == 0) && (m_left == 1) && (middle == 0) && (m_right == 0) && (right == 0))
        Error = 2;
    else if((left == 0) && (m_left == 1) && (middle == 1) && (m_right == 0) && (right == 0))
        Error = 1;
    else if((left == 0) && (m_left == 0) && (middle == 1) && (m_right == 0) && (right == 0))
        Error = 0;
    else if((left == 0) && (m_left == 0) && (middle == 1) && (m_right == 1) && (right == 0))
        Error = -1;
    else if((left == 0) && (m_left == 0) && (middle == 0) && (m_right == 1) && (right == 0))
        Error = -2;
    else if((left == 0) && (m_left == 0) && (middle == 0) && (m_right == 1) && (right == 1))
        Error = -3;
    else if((left == 0) && (m_left == 0) && (middle == 0) && (m_right == 0) && (right == 1))
        Error = -4;
    else if((left == 0) && (m_left == 0) && (middle == 0) && (m_right == 0) && (right == 0))
    {
        if (Previous_Error = -4) 
            Error = -5;
        else if (Previous_Error = 4)
            Error = 5;
        else
          Error = 9999;
    }
    else if((left == 1) && (m_left == 1) && (middle == 1) && (m_right == 1) && (right == 1))
        Error = 9999;
    Serial.println("Error: " + String(Error));
}

void Calculate_PID() 
{ 
    if(Error == 9999)
      return;
      
    P = Error;
    I += Error;
    //I = I + Previous_I;
    D = Error - Previous_Error;

    PID_value = (Kp * P) + (Ki * I) + (Kd * D);

    I += Error;
    Previous_I = I;
    Previous_Error = Error;
}

void MotorControl() 
{
    if(Error == 9999)
    {
      DcMotors::ActivateLeftMotor(0, true);
      DcMotors::ActivateRightMotor(0, true);
      return;
    }
    if ((-5 < Error) and (Error < 0)){
        Left_Speed  = LeftInitialSpeed - PID_value;
        Right_Speed = RightInitialSpeed + PID_value;
    }

    if ((0 < Error) and (Error < 5)){
        Left_Speed  = LeftInitialSpeed + PID_value;
        Right_Speed = RightInitialSpeed - PID_value;
    }

    if (Error == 0){
        Left_Speed  = LeftInitialSpeed;
        Right_Speed = RightInitialSpeed;
    }

    Serial.println("PID_Value: " + String(PID_value));
    Serial.println("Left_Speed: " + String(Left_Speed) + " | Right_Speed: " + String(Right_Speed));
    
    DcMotors::ActivateLeftMotor(Left_Speed, true);
    DcMotors::ActivateRightMotor(Right_Speed, true);
}
