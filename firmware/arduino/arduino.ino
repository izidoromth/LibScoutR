int time = 0;

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;

void setup() {
  Serial.begin(9600);
}

void loop() 
{
  boolean IRLeftData        = digitalRead(IRLeft);
  boolean IRMiddleLeftData  = digitalRead(IRMiddleLeft);
  boolean IRMiddleData      = digitalRead(IRMiddle);
  boolean IRMiddleRightData = digitalRead(IRMiddleRight);
  boolean IRRightData       = digitalRead(IRRight);
  
  unsigned long t = millis();
  
  Serial.println(String(t/1000) + ": " +  "Left: " + IRLeftData +  " Middle Left: " + IRMiddleLeftData +  " Middle: " + IRMiddleData +  " Middle Right: " + IRMiddleRightData +  " Right: " + IRRightData);
  
  delay(500);
}

void communicate()
{
  Serial.println("hi rasp");
  delay(100);// must be added.
  recvWithEndMarker();
  showNewData();
}

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            newData = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
        //Serial.println("This just in ... ");
        Serial.println(receivedChars);
        newData = false;
    }
}
