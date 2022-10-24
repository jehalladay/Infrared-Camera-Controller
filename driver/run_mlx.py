import sys, time

import board
import busio
import adafruit_mlx90640

from utils.csv_handling import (
    append_csv,
    create_csv
)

from utils.types import (
    Frame,
    Metadata,
    Picture
)

from MLX.scan_and_flip import (
    scan_and_flip
)

def main(file_name: str = './readingsCSV/test.csv', width: int = 32, height: int = 24, verbose: bool = False):
    '''
        This function will control the loop for operating the infrared camera
    '''

    columns = ['timestamp'] + [f'pixel_{i}' for i in range(width * height)]
    frame: Frame = []
    metadata: Metadata = []

    create_csv(
        file_name, 
        columns = columns,
        verbose = verbose 
    )

    while True:
        if verbose:
            print(f"Writing at {time.monotonic()}")
        
        try:
            frame, metadata = scan_and_flip(mlx, width = width, height = height, verbose = verbose)
            append_csv(file_name, frame, metadata = metadata)
            time.sleep(3)
        except ValueError:
            time.sleep(0.1)

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