import os, sys, time
import pandas as pd
import numpy as np

from cv2 import (
    VideoCapture
)

from utility import (
    create_csv,
    append_csv
)


def open_camera(cam_num: int = 0) -> VideoCapture:

    #Specifies first camera attached to RBPi. This needs fixing, How are the numbers assigned?
    cap = VideoCapture(cam_num) 
    
    if not cap.isOpened():
        raise IOError("Can't open IR-Mega Pixel Camera")

    return cap


def capture_frame(cap: VideoCapture):
    _, frame = cap.read()
    frame: np.ndarray = frame.reshape(-1)


def main(file_name: str = './readingsCSV/test.csv', width: int = 640, height: int = 480, channels: int = 3, verbose: bool = False):

    columns = ['timestamp'] + [f'pixel_{i}' for i in range(width * height * channels)]

    create_csv(
        file_name, 
        columns = columns,
        verbose = verbose 
    )

    cap = open_camera(cam_num = 0)

    while True:
        stamp = time.monotonic()

        if verbose:
            print(f"Writing at {stamp}")

        frame = capture_frame(cap)

        append_csv(file_name, frame, metadata = [stamp])
        
        time.sleep(3)


if __name__ == "__main__":
    date = time.strftime("%Y_%m_%d")

    file_name = f'./readingsCSV/fisheye_megapixel_{date}.csv'
    height = 480
    width = 640
    channels = 3
    verbose = False

    if len(sys.argv) > 1:
        file_name = sys.argv[1] 
    if len(sys.argv) > 2:
        width = int(sys.argv[2])
    if len(sys.argv) > 3:
        height = int(sys.argv[3])
    if len(sys.argv > 4):
        verbose = bool(int(sys.argv[4]))

    main(
        file_name = file_name, 
        width = width, 
        height = height, 
        channels = channels,
        verbose = verbose
    )




# Used libraries in guide: https://littlebirdelectronics.com.au/guides/165/set-up-opencv-on-raspberry-pi-4