import sys, os
import cv2
import numpy as np
import pyzbar
from pyzbar.pyzbar import decode, ZBarSymbol


"""  ----- Qr Code Detection -----

camera_address:         address of the camera
exposition_iterations:  how many frames to be captured
crop_top:               distance from top to be cropped
crop_bottom:            distance from bottom to be cropped
display_capture:        wether to display the preview window or not

returns a list with the codes detected, in order from left to right  """


def qr_detect(
    camera_address, exposition_iterations, crop_top, crop_bottom, display_capture
):

    if display_capture:
        cv2.namedWindow("preview")

    # open camera feed
    vc = cv2.VideoCapture(camera_address)

    # try to get the first frame
    if vc.isOpened():
        rval, img = vc.read()
    else:
        rval = False

    detected_qr_list = []
    iterations_count = 0
    while rval and iterations_count < exposition_iterations:
        iterations_count += 1

        # crop image
        height, width, channels = img.shape
        img = img[crop_top : height - crop_bottom, 0:width]

        # detect qr codes
        decoded = decode(img, symbols=[ZBarSymbol.QRCODE])

        for qr in decoded:
            # get info for each qr code
            text_qr = qr.data.decode("utf-8")
            points = np.array(qr.polygon, np.int32)
            x_pos, y_pos = points[1]

            # check if qr already exists in the list
            if not (
                text_qr in (item for sublist in detected_qr_list for item in sublist)
            ):
                # add text and x position to list
                detected_qr_list.append([text_qr, x_pos])
                # order detected qr list
                detected_qr_list.sort(key=lambda x: x[1])

            if display_capture:
                # draw polygon
                cv2.polylines(img, [points], 1, (255, 0, 0), 4)
                # draw text
                cv2.putText(
                    img,
                    text_qr,
                    (x_pos, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (0, 0, 0),
                    4,
                )

        if display_capture:
            # draw list of detected codes at top left corner
            i = 0
            for qr in detected_qr_list:
                cv2.putText(
                    img,
                    qr[0],
                    (5, 25 + i),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 0, 255),
                    2,
                )
                i += 25

            cv2.imshow("preview", img)
            key = cv2.waitKey(1)

        rval, img = vc.read()

    # prepare output list
    out_list = []
    out_list = [qr[0] for qr in detected_qr_list]

    return out_list


# Usage example
print(
    qr_detect(
        camera_address=0,
        exposition_iterations=50,
        crop_top=80,
        crop_bottom=230,
        display_capture=True,
    )
)
