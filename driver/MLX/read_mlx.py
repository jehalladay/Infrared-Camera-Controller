'''
    File controls the infrared camera and saves each frame to a csv file

    If called from the command line, it will expect the following arguments following the file name:
        1. file_name: the name of the csv file to save the data to
        2. width: the width of the camera
        3. height: the height of the camera
        4. verbose: whether or not to print the data to the console
'''

import time
from typing import Tuple
import numpy as np

from utils.types import (
    Frame,
    Metadata,
    Picture
)

from utils.csv_handling import (
    create_csv,
    append_csv
)

def read_mlx(
    mlx, 
    width: int = 32, 
    height: int = 24,
    channels: int = 1,
    precision: int = 2,
    verbose: bool = False
) -> Picture:
    '''
        This function will scan the MLX90640 and flip the data
        The data will be appended to the csv file
    '''
    
    stamp = time.monotonic()
    frame = [0] * width * height * channels

    mlx.getFrame(frame)
    frame = [round(x, precision) for x in frame]
    start, end = 0, width
    
    for i in range(height * channels):
        frame[start:end] = frame[start:end][::-1]
        start += width
        end += width
        
    if verbose:
        print(f"print@ {stamp}\n{frame}\n\n")
    
    return frame, [stamp]
