import json, os, sys, time
import pandas as pd
import numpy as np

from pathlib import (
    Path
)

from cv2 import (
    imwrite
)

from MP.cam import (
    open_camera,
    capture_frame
)

from utils.constants import (
    MP_CONFIG_JSON,
    STORAGE,
    RECORDING,
    LOCATION,
    PATH,
    FREQUENCY,
    DURATION,
    DATE_FORMAT,
    TIME_FORMAT
)


def main(
    file_name: str  = './data/test_{time}.png', 
    duration : int  = 120,
    frequency: int  = 3,
    verbose  : bool = False
) -> None:
    '''
        This function will control the loop for operating the MP camera
        The camera simply sends us a frame at the desired frequency
            and the frame is saved to an image file with a unique file name
    '''

    frame = []

    cap = open_camera(cam_num = 0)

    while duration > 0:
        if verbose:
            print(f"Writing at {time.monotonic()}")
        
        frame = capture_frame(cap)
        
        imwrite(
            # if file_name contains the substring {time}, it will be replaced with the current time
            #   this will allow for subsequent frames to be saved with unique and ordered names
            file_name.format(time = time.strftime(TIME_FORMAT)), 
            frame
        )

        duration -= frequency
        time.sleep(frequency)


if __name__ == '__main__':

    # get todays date
    date = time.strftime(DATE_FORMAT)

    # load config from ./config/mp.json
    config: dict = json.load(open(MP_CONFIG_JSON, 'r'))
    
    file_path = config[STORAGE][PATH].format(
        date = date
    )

    file_name = file_path + config[STORAGE][LOCATION]

    if not Path(file_path).exists():
        os.makedirs(file_path)

    verbose = False
    
    duration  = float(config[RECORDING][DURATION])
    frequency = float(config[RECORDING][FREQUENCY])

    if len(sys.argv) > 1:
        file_name = sys.argv[1] 
    if len(sys.argv) > 2:
        width = int(sys.argv[2])
    if len(sys.argv) > 3:
        height = int(sys.argv[3])
    if len(sys.argv) > 4:
        verbose = bool(int(sys.argv[4]))

    print(f"Running MP Fisheye Camera for {duration} seconds at {1/frequency} Hz")

    main(
        file_name = file_name,
        duration = duration,
        frequency = frequency,
        verbose = verbose
    )

    print("MP: Done")
