#include <Wire.h>
#include <SparkFun_APDS9960.h>
#include "dc_motors.h"
#include "ir_sensor.h"

#define RightInitialSpeed 105
#define LeftInitialSpeed 105

#define Kp_fw 3
#define Ki_fw 0
#define Kd_fw 46

#define Kp_bw 1
#define Ki_bw 0
#define Kd_bw 10

#define momentum 1.4
#define ang_momentum 1.25

float P = 0;
float I = 0;
float D = 0;
int Error = 0;

int Previous_Error, Previous_I;
int PID_value;
int Left_Speed, Right_Speed;

boolean mov_direction = true;

SparkFun_APDS9960 apds = SparkFun_APDS9960();
uint16_t ambient_light = 0;
uint16_t red_light = 0;
uint16_t green_light = 0;
uint16_t blue_light = 0;

char commandBuffer[6];
int timeout_loops = 0;

void setup()
{
    Serial.begin(9600);
    Serial.setTimeout(5000);
    serialFlush();

    pinMode(LED_BUILTIN, OUTPUT);
    
    DcMotors::Init();
    IRSensor::Init();

  /*
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
  */

    clearCommandBuffer();
    serialFlush();
    // Wait for initialization and calibration to finish
    delay(500);

    //DcMotors::ActivateLeftMotor(200, true);
    //DcMotors::ActivateRightMotor(200, true);
    delay(100);
}

void loop() 
{
  Serial.readBytesUntil('\n',commandBuffer, 6);  
  serialFlush();

  //Calls rotate subroutine
  if(commandBuffer[3] != 's')
  {
    if(commandBuffer[3] == 'p')
    {
      Rotate(1, true, mov_direction);
    }
    else if(commandBuffer[3] == 'n')
    {
      Rotate(1, false, mov_direction);
    }
    else if(commandBuffer[3] == 'c')
    {
      Rotate(2, true, mov_direction);
    }
  }

  delay(500);

  //Checks if scan is needed
  if(commandBuffer[4] == 'y')
  {
    boolean cornerFound = false;
    while(!cornerFound)
    {      
      cornerFound = MoveByTime(1000);

      if(!cornerFound)
      {
        Serial.write("okay_eol");
        Serial.flush();
  
        do
        {
          clearCommandBuffer();
          serialFlush();
          Serial.readBytesUntil('\n',commandBuffer, 6);
        }
        while(commandBuffer[0] != 'n' && commandBuffer[0] != 'e' && commandBuffer[0] != 'x' && commandBuffer[0] != 't');
      }
    }
    Serial.write("final_eol");
    Serial.flush();
  }
  else if(commandBuffer[4] == 'n')
  {
    MoveUntilNextCorner();
    Serial.write("final_eol");
    Serial.flush();
  }

  clearCommandBuffer();
}
                                                                                                                                                                 
void CalculateError(boolean dir)
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
      
    //Serial.println("Error: " + String(Error));
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

  //Serial.println("PID_Value: " + String(PID_value));
  //Serial.println("Left_Speed: " + String(Left_Speed) + " | Right_Speed: " + String(Right_Speed));
  
  DcMotors::ActivateLeftMotor(Left_Speed, dir);
  DcMotors::ActivateRightMotor(Right_Speed, dir);
}

boolean FollowLine(boolean dir)
{
  CalculateError(dir);
  if(Error == 9999)
  {
    PID_value = 0;
    P = 0;
    I = 0;
    D = 0;
    Previous_I = 0;
    Previous_Error = 0;
    DcMotors::ActivateLeftMotor(0, true);
    DcMotors::ActivateRightMotor(0, true);
    return true;
  }
  Calculate_PID(dir);
  MotorControl(dir);
  return false;
}

void ReadRGB()
{
  if(!apds.readAmbientLight(ambient_light) || !apds.readRedLight(red_light) || !apds.readGreenLight(green_light) || !apds.readBlueLight(blue_light))
  {
    //Serial.println("Error reading light values");
  } 
  else 
  {
    /*
    Serial.print("Ambient: ");
    Serial.print(ambient_light);
    Serial.print(" Red: ");
    Serial.print(red_light);
    Serial.print(" Green: ");
    Serial.print(green_light);
    Serial.print(" Blue: ");
    Serial.println(blue_light);
    */
  }
}

boolean MoveByTime(int milliseconds)
{
  unsigned long initialTime = millis();
  if(commandBuffer[0] == 'f')
  {
    mov_direction = true;
  }
  else if(commandBuffer[0] == 'b')
  {
    mov_direction = false;
  }
  DcMotors::ActivateLeftMotor(LeftInitialSpeed*momentum, mov_direction);
  DcMotors::ActivateRightMotor(RightInitialSpeed*momentum, mov_direction);
  delay(400);
  while(millis() - initialTime < milliseconds)
  {
    if(FollowLine(mov_direction))
      return true;
  }
  DcMotors::ActivateLeftMotor(0, false);
  DcMotors::ActivateRightMotor(0, false);
  return false;
}

void MoveUntilNextCorner()
{
  if(commandBuffer[0] == 'f')
  {
    mov_direction = true;
  }
  else if(commandBuffer[0] == 'b')
  {
    mov_direction = false;
  }
  DcMotors::ActivateLeftMotor(LeftInitialSpeed*momentum, mov_direction);
  DcMotors::ActivateRightMotor(RightInitialSpeed*momentum, mov_direction);
  delay(400);
  while(!FollowLine(mov_direction));
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

  DcMotors::ActivateLeftMotor(LeftInitialSpeed*ang_momentum, !angular_dir);
  DcMotors::ActivateRightMotor(RightInitialSpeed*ang_momentum, angular_dir);

  delay(300);
  
  while(steps < ninety_steps)
  {
    ticks = 0;
    
    boolean left;
    boolean m_left;
    boolean middle;
    boolean m_right;
    boolean right;

    /*if(!IRSensor::ReadMiddle() == 0)
    {
      do
      {
        left = !IRSensor::ReadLeft();
        m_left = !IRSensor::ReadMiddleLeft();
        middle = !IRSensor::ReadMiddle();
        m_right = !IRSensor::ReadMiddleRight();
        right = !IRSensor::ReadRight();
        ticks++;
        delay(25);
      }
      while(middle != 1);
    }
    
    do
    {
      left = !IRSensor::ReadLeft();
      m_left = !IRSensor::ReadMiddleLeft();
      middle = !IRSensor::ReadMiddle();
      m_right = !IRSensor::ReadMiddleRight();
      right = !IRSensor::ReadRight();
      ticks++;      
      delay(25);
    }
    while(middle == 1);*/

    do
    {
      left = !IRSensor::ReadLeft();
      m_left = !IRSensor::ReadMiddleLeft();
      middle = !IRSensor::ReadMiddle();
      m_right = !IRSensor::ReadMiddleRight();
      right = !IRSensor::ReadRight();
      ticks++;
      delay(25);
    }
    while(middle != 1);
    //while(!((angular_dir && middle != 1 && m_left != 1) || (!angular_dir && middle != 1 && m_right != 1)));
    
    steps++;
  }

  DcMotors::ActivateLeftMotor(0, false);
  DcMotors::ActivateRightMotor(0, false);
}

void clearCommandBuffer()
{
  for(int i = 0; i < 6; i++)
    commandBuffer[i] = 0;
}

void serialFlush(){
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
}
