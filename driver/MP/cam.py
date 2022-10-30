import numpy as np

from cv2 import (
    VideoCapture
)


def open_camera(cam_num: int = 0) -> VideoCapture:
    #Specifies the camera attached to RBPi. This needs fixing, How are the numbers assigned?
    cap = VideoCapture(cam_num) 

    if not cap.isOpened():
        raise IOError("Can't open Mega Pixel Camera")

    return cap


def capture_frame(cap: VideoCapture):
    _, frame = cap.read()
    cap.release()

    return frame

