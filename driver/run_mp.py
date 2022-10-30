import json, os, sys, time
import pandas as pd
import numpy as np

from cv2 import (
    VideoCapture
)

from utils.csv_handling import (
    append_csv,
    create_csv
)

from utils.types import (
    Frame,
    Metadata
)

from utils.constants import (
    MP_CONFIG_JSON,
    SIZE,
    STORAGE,
    RECORDING,
    WIDTH,
    HEIGHT,
    CHANNELS,
    PRECISION,
    LOCATION,
    PATH,
    FREQUENCY,
    DURATION,
    DATE_FORMAT,
    TIME_FORMAT,
    STALL_TIME
)


def main(
    file_name: str  = './readingsCSV/test.csv', 
    width    : int  = 32, 
    height   : int  = 24,
    channels : int  = 1,
    precision: int  = 2,
    duration : int  = 120,
    frequency: int  = 3,
    verbose  : bool = False
) -> None:
    '''
        This function will control the loop for operating the infrared camera
    '''

    columns: list = ['timestamp'] + [f'pixel_{i}' for i in range(width * height * channels)]
    frame: Frame = []
    metadata: Metadata = []

    create_csv(
        file_name, 
        columns = columns,
        verbose = verbose 
    )

    while duration > 0:
        if verbose:
            print(f"Writing at {time.monotonic()}")
        
        try:

            append_csv(file_name, frame, metadata = metadata)
            duration -= frequency
            time.sleep(frequency)

        except ValueError:
            time.sleep(STALL_TIME)

            # double the stall time because time passed in the try block
            duration -= STALL_TIME * 2 


if __name__ == '__main__':

    # get todays date
    date = time.strftime(DATE_FORMAT)
    timestamp = time.strftime(TIME_FORMAT)

    # load config from ./config/mlx.json
    config: dict = json.load(open(MP_CONFIG_JSON, 'r'))
    
    file_path = config[STORAGE][PATH]
    file_name = file_path + config[STORAGE][LOCATION]

    file_name = file_name.format(
        date = date, 
        time = timestamp
    )

    verbose = False
    
    width     = int(config[SIZE][WIDTH])
    height    = int(config[SIZE][HEIGHT])
    channels  = int(config[SIZE][CHANNELS])
    precision = int(config[STORAGE][PRECISION])

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

    print(f"Running MLX Infrared Camera for {duration} seconds at {1/frequency} Hz")

    main(
        file_name = file_name, 
        width = width, 
        height = height,
        channels = channels,
        precision = precision,
        duration = duration,
        frequency = frequency,
        verbose = verbose
    )

    print("MLX: Done")
