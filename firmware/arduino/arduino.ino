#include "ArduinoJson.h"

const int interval = 1000;
int currentTime = 0;
int lastTime = 0;
bool ledState = false;

// the setup function runs once when you press reset 
// or power the board
void setup() 
{
    // initialize digital pin LED_BUILTIN as an output.
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() 
{
    currentTime = millis();
    if(currentTime - lastTime >= interval)
    {
      lastTime = currentTime;

      ledState = !ledState;

      if(ledState)
        digitalWrite(LED_BUILTIN, HIGH);
      else
        digitalWrite(LED_BUILTIN, LOW);
    }
    
    test();
}

void test()
{
  // Put the JSON input in memory (shortened)
  String input = "{\"name\":\"ArduinoJson\"}";
  
  // Compute the required size
  const int capacity = JSON_ARRAY_SIZE(2)+ 2*JSON_OBJECT_SIZE(3)+ 4*JSON_OBJECT_SIZE(1);
  
  // Allocate the JsonDocument
  StaticJsonDocument<capacity> doc;
  
  // Parse the JSON input
  DeserializationError err = deserializeJson(doc, input);
  
  // Parse succeeded?
  if (err) 
  {
    Serial.print(F("deserializeJson() returned "));
    Serial.println(err.c_str());
  }
  else
  {
    Serial.println("Tudo certin");
    String name = doc["name"];
    Serial.println(name);
  }
}
