from cv2 import(
    VideoCapture,
    imwrite
)
from time import sleep

cap = VideoCapture(0) #Specifies first camera attached to RBPi. This needs fixing, How are the numbers assigned?
if not cap.isOpened():
    raise IOError("Can't open IR-Mega Pixel Camera")
for i in range(6):
    print(f"image: {i+1}, in 2 seconds")
    sleep(1)
    ret, frame = cap.read() #Capture a frame
    out = imwrite(f"./images/capture_{i}.jpg", frame)
    cap.release()
    cap = VideoCapture(0)

# Used libraries in guide: https://littlebirdelectronics.com.au/guides/165/set-up-opencv-on-raspberry-pi-4