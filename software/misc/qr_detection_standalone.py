import sys, os
import cv2
import numpy as np
import pyzbar
from pyzbar.pyzbar import decode, ZBarSymbol

DISPLAY_CAPTURE = True

if(DISPLAY_CAPTURE):
    cv2.namedWindow("preview")

# open camera feed
vc = cv2.VideoCapture('http://192.168.0.2:8080/video')

# try to get the first frame
if vc.isOpened():
    rval, img = vc.read()
else:
    rval = False

detected_qr_list = []
while rval:
    # detect qr codes
    decoded = decode(img, symbols=[ZBarSymbol.QRCODE])


    for qr in decoded:
        # get info for each qr code
        text_qr = qr.data.decode("utf-8")
        points = np.array(qr.polygon, np.int32)
        x_pos, y_pos = points[1]

        # check if qr already exists in the list
        if not (text_qr in (item for sublist in detected_qr_list for item in sublist)):
            # add text and x position to list
            detected_qr_list.append([text_qr, x_pos])
            # order detected qr list
            detected_qr_list.sort(key=lambda x: x[1])

        if (DISPLAY_CAPTURE):
            # draw polygon
            cv2.polylines(img, [points], 1, (255,0,0),4)
            # draw text
            cv2.putText(img, text_qr, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 0), 4)


    if (DISPLAY_CAPTURE):
        # draw list of detected codes at top left corner
        i=0
        for qr in detected_qr_list:
            cv2.putText(img, qr[0], (5,25+i), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 0, 255), 2)
            i+=25

        cv2.imshow("preview", img)
        key = cv2.waitKey(1)

    # prepare output list
    out_list = []
    out_list = [qr[0] for qr in detected_qr_list]

    rval, img = vc.read()
