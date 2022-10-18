'''
    File controls the infrared camera and saves each frame to a csv file

    If called from the command line, it will expect the following arguments following the file name:
        1. file_name: the name of the csv file to save the data to
        2. width: the width of the camera
        3. height: the height of the camera
        4. verbose: whether or not to print the data to the console
'''

import time
import numpy as np
from ..utility import (
    create_csv,
    append_csv
)

def scan_and_flip(file_name: str, mlx, width: int = 32, height: int = 24, verbose: bool = False):
    '''
        This function will scan the MLX90640 and flip the data
        The data will be appended to the csv file

        !! Cannot be called by outside files, else the mlx object will not exist
    '''
    stamp = time.monotonic()
    frame = [0] * width * height
    try: 
        mlx.getFrame(frame)
        frame = ['%.2f' % x for x in frame]
        start, end = 0, width
        
        for i in range(height):
            frame[start:end] = frame[start:end][::-1]
            start += width
            end += width
            
        if verbose:
            print(f"print@ {stamp}\n{frame}\n\n")
        append_csv(file_name, frame, metadata = [stamp])
    except ValueError:
        pass
