import serial
import time
import cv2

# Serial communication

# ser = serial.Serial('/dev/ttyACM0', 9600)
# ser.flushInput()

# while True:
#     s = ser.readline()
#     s = s.strip()

#     print(s.decode("utf-8"))

#     if (s.decode("utf-8") == "hi rasp"):
#         print("sending")
#         ans = "hello arduino\n"
#         ans = ans.encode("utf-8")
#         ser.write(ans)

raspicam = cv2.VideoCapture(0)
webcam = cv2.VideoCapture(1)
while True:
    raspicam_ret, raspicam_frame = raspicam.read()
    webcam_ret, webcam_frame = webcam.read()

    cv2.imshow("raspicam", raspicam_frame)
    cv2.imshow("webcam", webcam_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

raspicam.release()
# webcam.release()
cv2.destroyAllWindows()
