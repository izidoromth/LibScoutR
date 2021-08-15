#include <Wire.h>
#include <SparkFun_APDS9960.h>
#include "dc_motors.h"
#include "ir_sensor.h"

#define RightInitialSpeed 100
#define LeftInitialSpeed 100

#define Kp_fw 2
#define Ki_fw 0
#define Kd_fw 36

#define Kp_bw 1
#define Ki_bw 0
#define Kd_bw 10

#define momentum 1.4

float P = 0;
float I = 0;
float D = 0;
int Error = 0;

int Previous_Error, Previous_I;
int PID_value;
int Left_Speed, Right_Speed;

boolean mov_direction;

SparkFun_APDS9960 apds = SparkFun_APDS9960();
uint16_t ambient_light = 0;
uint16_t red_light = 0;
uint16_t green_light = 0;
uint16_t blue_light = 0;

void setup()
{
    Serial.begin(9600);
    
    DcMotors::Init();
    IRSensor::Init();

    if(apds.init())
    {
      Serial.println(F("APDS-9960 initialization complete"));
    } 
    else 
    {
      Serial.println(F("Something went wrong during APDS-9960 init!"));
    }
  
    // Start running the APDS-9960 light sensor (no interrupts)
    if(apds.enableLightSensor(false)) 
    {
      Serial.println(F("Light sensor is now running"));
    }
    else
    {
      Serial.println(F("Something went wrong during light sensor init!"));
    }
  
    // Wait for initialization and calibration to finish
    delay(500);

    //DcMotors::ActivateLeftMotor(200, true);
    //DcMotors::ActivateRightMotor(200, true);
    delay(100);
}

void loop() 
{
  char a;
  while(Serial.available() <= 0);

  a = Serial.read();
  if(a == 'w')
  {
    mov_direction = true;
    DcMotors::ActivateLeftMotor(LeftInitialSpeed*momentum, mov_direction);
    DcMotors::ActivateRightMotor(RightInitialSpeed*momentum, mov_direction);
    delay(400);
    while(FollowLine(mov_direction));
  }
  else if(a == 's')
  {
    mov_direction = false;
    DcMotors::ActivateLeftMotor(LeftInitialSpeed*momentum, mov_direction);
    DcMotors::ActivateRightMotor(RightInitialSpeed*momentum, mov_direction);
    delay(400);
    while(FollowLine(mov_direction));
  }
  else if(a == 'd')
  {
    Rotate(1, true, mov_direction);
  }
  else if(a == 'a')
  {
    Rotate(1, false, mov_direction);
  }    
  else if(a == 'f')
  {
    Rotate(2, true, mov_direction);
  }
  else if(a == 'q')
  {
    Rotate(2, false, mov_direction);
  }    
}
                                                                                                                                                                 
void CalculateError(boolean dir)
{
    boolean left = !IRSensor::ReadLeft();
    boolean m_left = !IRSensor::ReadMiddleLeft();
    boolean middle = !IRSensor::ReadMiddle();
    boolean m_right = !IRSensor::ReadMiddleRight();
    boolean right = !IRSensor::ReadRight();
    
    Serial.println("U1: " + String(left) + " | U2: " + String(m_left) + " | U3: " + String(middle) + " | U4: " + String(m_right) + " | U5: " + String(right));

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
    else if((left == 1) && (m_left == 1) && (middle == 1) && (m_right == 0) && (right == 0))
        Error = 9999;
    else if((left == 0) && (m_left == 0) && (middle == 1) && (m_right == 1) && (right == 1))
        Error = 9999;
      
    Serial.println("Error: " + String(Error));
}

void Calculate_PID(boolean dir) 
{       
  P = Error;
  I += Error;
  D = Error - Previous_Error;

  if(dir)
    PID_value = (Kp_fw * P) + (Ki_fw * I) + (Kd_fw * D);
  else
    PID_value = (Kp_bw * P) + (Ki_bw * I) + (Kd_bw * D);

  Previous_I = I;
  Previous_Error = Error;
}

void MotorControl(boolean dir) 
{
  if (Error == 0){
      Left_Speed  = LeftInitialSpeed;
      Right_Speed = RightInitialSpeed;
  }
  else if(dir)
  {
      Left_Speed  = LeftInitialSpeed - PID_value;
      Right_Speed = RightInitialSpeed + PID_value;
  }
  else
  {
      Left_Speed  = LeftInitialSpeed - PID_value;
      Right_Speed = RightInitialSpeed + PID_value;
  }

  Serial.println("PID_Value: " + String(PID_value));
  Serial.println("Left_Speed: " + String(Left_Speed) + " | Right_Speed: " + String(Right_Speed));
  
  DcMotors::ActivateLeftMotor(Left_Speed, dir);
  DcMotors::ActivateRightMotor(Right_Speed, dir);
}

boolean FollowLine(boolean dir)
{
  CalculateError(dir);  
  //ReadRGB();
  if(Error == 9999/* || (red_light> 100 || green_light > 100 || blue _light > 100)*/)
  {
    PID_value = 0;
    P = 0;
    I = 0;
    D = 0;
    Previous_I = 0;
    Previous_Error = 0;
    DcMotors::ActivateLeftMotor(0, true);
    DcMotors::ActivateRightMotor(0, true);
    return false;
  }
  Calculate_PID(dir);
  MotorControl(dir);
  return true;
}

void ReadRGB()
{
  if(!apds.readAmbientLight(ambient_light) || !apds.readRedLight(red_light) || !apds.readGreenLight(green_light) || !apds.readBlueLight(blue_light))
  {
    //Serial.println("Error reading light values");
  } 
  else 
  {
    /*Serial.print("Ambient: ");
    Serial.print(ambient_light);
    Serial.print(" Red: ");
    Serial.print(red_light);
    Serial.print(" Green: ");
    Serial.print(green_light);
    Serial.print(" Blue: ");
    Serial.println(blue_light);*/
  }
}

void Rotate(int ninety_steps, boolean angular_dir, boolean previous_dir)
{
  int steps = 0;
  int ticks = 0;
  
  if(!previous_dir)
  {
    DcMotors::ActivateLeftMotor(LeftInitialSpeed*momentum, true);
    DcMotors::ActivateRightMotor(RightInitialSpeed*momentum, true);

    delay(350);

    DcMotors::ActivateLeftMotor(0, false);
    DcMotors::ActivateRightMotor(0, false);
  }
  else
  {
    DcMotors::ActivateLeftMotor(LeftInitialSpeed*momentum, true);
    DcMotors::ActivateRightMotor(RightInitialSpeed*momentum, true);

    delay(350);

    DcMotors::ActivateLeftMotor(0, false);
    DcMotors::ActivateRightMotor(0, false);
  }

  DcMotors::ActivateLeftMotor(LeftInitialSpeed*momentum, !angular_dir);
  DcMotors::ActivateRightMotor(RightInitialSpeed*momentum, angular_dir);
  
  while(steps < ninety_steps)
  {
    ticks = 0;
    
    boolean left;
    boolean m_left;
    boolean middle;
    boolean m_right;
    boolean right;
    
    do
    {
      left = !IRSensor::ReadLeft();
      m_left = !IRSensor::ReadMiddleLeft();
      middle = !IRSensor::ReadMiddle();
      m_right = !IRSensor::ReadMiddleRight();
      right = !IRSensor::ReadRight();
      Serial.println("While 1");
      ticks++;
    }
    while(middle == 1 && ticks < 100);

    do
    {
      left = !IRSensor::ReadLeft();
      m_left = !IRSensor::ReadMiddleLeft();
      middle = !IRSensor::ReadMiddle();
      m_right = !IRSensor::ReadMiddleRight();
      right = !IRSensor::ReadRight();
      Serial.println("While 2:");
      ticks++;
    }
    while(middle != 1 && ticks < 100);
    //while(!((angular_dir && middle != 1 && m_left != 1) || (!angular_dir && middle != 1 && m_right != 1)) && ticks < 100);
    
    steps++;

    //delay(150);
  }

  DcMotors::ActivateLeftMotor(0, false);
  DcMotors::ActivateRightMotor(0, false);
}
