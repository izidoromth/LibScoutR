import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.flushInput()

while True:
    s = ser.readline()
    s = s.strip()
    
    print(s.decode("utf-8"))

    if (s.decode("utf-8") == "hi rasp"):
        print("sending")
        ans = "hello arduino\n"
        ans = ans.encode("utf-8")
        ser.write(ans)
