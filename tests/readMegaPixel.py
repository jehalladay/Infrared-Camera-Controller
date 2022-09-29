import cv2
import time

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Can't open IR-Mega Pixel Camera")

for i in range(5):
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=.75, fy=0.5)
    out = cv2.imwrite(f"capture_{i}.jpg", frame)
    time.sleep(3)


# Used libraries in guide: https://littlebirdelectronics.com.au/guides/165/set-up-opencv-on-raspberry-pi-4