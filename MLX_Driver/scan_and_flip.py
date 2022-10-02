'''
    File controls the infrared camera and saves each frame to a csv file

    If called from the command line, it will expect the following arguments following the file name:
        1. file_name: the name of the csv file to save the data to
        2. width: the width of the camera
        3. height: the height of the camera
        4. verbose: whether or not to print the data to the console
'''

import sys, time

import board
import busio
import adafruit_mlx90640

import numpy as np

from utility import (
    create_csv,
    append_csv
)


def scan_and_flip(file_name: str, width: int = 32, height: int = 24, verbose: bool = False):
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


def main(file_name: str = './readingsCSV/test.csv', width: int = 32, height: int = 24, verbose: bool = False):
    '''
        This function will control the loop for operating the infrared camera
    '''

    columns = ['timestamp'] + [f'pixel_{i}' for i in range(width * height)]

    create_csv(
        file_name, 
        columns = columns,
        verbose = verbose 
    )

    while True:
        if verbose:
            print(f"Writing at {time.monotonic()}")

        scan_and_flip(file_name, width = width, height = height, verbose = verbose)
        
        time.sleep(3)


if __name__ == '__main__':

    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    mlx = adafruit_mlx90640.MLX90640(i2c)
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_32_HZ

    print("MLX addr detected on I2C")
    print([hex(i) for i in mlx.serial_number])

    # get todays date
    date = time.strftime("%Y_%m_%d")

    file_name = f'./readingsCSV/infrared_{date}.csv'
    height = 24
    width = 32
    channels = 1
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
        verbose = verbose
    )

