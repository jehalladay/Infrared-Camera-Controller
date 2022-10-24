import json, sys, time

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

from utils.constants import (
    MLX_CONFIG_JSON,
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
    DATE_FORMAT
)

from MLX.scan_and_flip import (
    scan_and_flip
)

def main(
    file_name: str = './readingsCSV/test.csv', 
    width: int = 32, 
    height: int = 24,
    channels: int = 1,
    precision: int = 2,
    duration: int = 120,
    frequency: int = 3,
    verbose: bool = False
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
            frame, metadata = scan_and_flip(
                mlx, 
                width = width, 
                height = height, 
                channels = channels,
                precision = precision,
                verbose = verbose
            )

            append_csv(file_name, frame, metadata = metadata)
            duration -= frequency
            time.sleep(frequency)

        except ValueError:
            duration -= 0.1
            time.sleep(0.1)

if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    mlx = adafruit_mlx90640.MLX90640(i2c)
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_32_HZ

    print("MLX addr detected on I2C")
    print([hex(i) for i in mlx.serial_number])

    # get todays date
    date = time.strftime(DATE_FORMAT)

    # load config from ./config/mlx.json
    config: dict = json.load(open(MLX_CONFIG_JSON, 'r'))
    
    file_path = config[STORAGE][PATH]
    file_name = file_path + config[STORAGE][LOCATION].format(date=date)

    verbose = False
    width = config[SIZE][WIDTH]
    height = config[SIZE][HEIGHT]
    channels = config[SIZE][CHANNELS]
    precision = config[STORAGE][PRECISION]
    duration = config[RECORDING][DURATION]
    frequency = config[RECORDING][FREQUENCY]

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
        precision = precision,
        duration = duration,
        frequency = frequency,
        verbose = verbose
    )