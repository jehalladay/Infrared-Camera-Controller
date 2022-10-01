import cv2top

import time

cap = cv2.VideoCapture(0) #Specifies first camera attached to RBPi. This needs fixing, How are the numbers assigned?
if not cap.isOpened():
    raise IOError("Can't open IR-Mega Pixel Camera")

for i in range(5):
    ret, frame = cap.read() #Capture a frame
    out = cv2.imwrite(f"capture_{i}.jpg", frame)
    time.sleep(3)

# Used libraries in guide: https://littlebirdelectronics.com.au/guides/165/set-up-opencv-on-raspberry-pi-4