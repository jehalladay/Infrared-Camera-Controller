import board, busio, json, sys, time

import numpy as np

import adafruit_mlx90640

from adafruit_as726x import (
    AS726x_I2C
)

from AS.readSpectro import (
    readSpectro
)

from cv2 import (
    imwrite
)

from MP.cam import (
    open_camera,
    capture_frame
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
    CHANNELS,
    COLOR_CHANNELS,
    DATE_FORMAT,
    DATE_FORMAT,
    HEIGHT,
    LOCATION,
    MODE,
    MP,
    MLX,
    ONCE_CONFIG_JSON,
    PATH,
    PRECISION,
    SIZE,
    TIME_FORMAT,
    SP,
    SPECTRO_CONFIG_JSON,
    SPECTRO_ADDRESS,
    SPECTRO_GPIO,
    STORAGE,
    RUN,
    WIDTH
)

from MLX.read_mlx import (
    read_mlx
)

def main(
    mlx, spectro,
    file_path    : str  = './readingsCSV/test.csv', 
    run_mlx      : bool = True,
    run_sp  : bool = True,
    run_mp       : bool = True,
    columns      : list = ['violet', 'blue', 'green', 'yellow', 'orange', 'red'],
    verbose      : bool = False
) -> None:
    '''
        This function will control the loop for operating the infrared camera
    '''

    columns: list = ['timestamp'] + columns

    create_csv(
        file_path + "infra_spectro.csv", 
        columns = columns,
        verbose = verbose 
    )

    if verbose:
        print(f"Writing at {time.monotonic()}")
    
    if run_mlx:
        mlx_frame: Frame = []
        mlx_metadata: Metadata = []
        flag = True

        while flag:
            try:
                #GPIO set here
                mlx_frame, metadata = read_mlx(
                    mlx, 
                    width = 32, 
                    height = 24, 
                    channels = 1,
                    verbose = verbose
                )

            except:
                continue
            mlx_columns: list = ['timestamp'] + [f'pixel_{i}' for i in range(32 * 24)]

            create_csv(
                file_path + "infrared.csv", 
                columns = mlx_columns,
                verbose = verbose 
            )
            # print(type(mlx_frame))
            # print(mlx_frame.size)
            # print(mlx_frame.shape)
            # print(mlx_frame)

            # imwrite(
            #     file_path + "mlx.png",
            #     np.asarray(mlx_frame).reshape((24, 32))
            # )

            append_csv(file_path + 'infrared.csv', mlx_frame, metadata = metadata)
            flag = False

    if run_mp:
        flag = True

        while flag:
            mp_frame = capture_frame(open_camera(cam_num = 0))

            if type(mp_frame) != type(None) and mp_frame.size > 0 :
                imwrite(
                    # if file_name contains the substring {time}, it will be replaced with the current time
                    #   this will allow for subsequent frames to be saved with unique and ordered names
                    file_path + "mp.png",
                    mp_frame
                )

                flag = False

    if run_sp:

        if verbose:
            print(f"Reading at {time.monotonic()}")
        #GPIO HERE

        sp_frame = readSpectro(
            spectro, 
            True, 
            columns = columns
        )
        
        append_csv(
            file_path + "infra_spectro.csv",
            data      = sp_frame, 
            metadata  = [time.strftime(TIME_FORMAT)]
        )



if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    mlx = adafruit_mlx90640.MLX90640(i2c)
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_32_HZ

    # activate the RBPi default SCL and SDA pins
    i2c = board.I2C()

    # Spectrometer address at 0x49, set inside utils/constants.py
    spectro = AS726x_I2C(i2c, SPECTRO_ADDRESS) 

    # get todays date
    date = time.strftime(DATE_FORMAT)
    timestamp = time.strftime(TIME_FORMAT)

    if len(sys.argv) > 1:
        verbose = bool(int(sys.argv[2]))

    # load config from ./config/mlx.json
    config: dict = json.load(open(ONCE_CONFIG_JSON, 'r'))
    
    file_path = config[STORAGE][PATH]

    file_path = file_path.format(
        date = date, 
        time = timestamp
    )

    verbose = False
    
    run_MP  = bool(int(config[MP][RUN]))
    run_MLX = bool(int(config[MLX][RUN]))
    run_SP  = bool(int(config[SP][RUN]))


    channels: dict = config[SP][COLOR_CHANNELS]

    columns = []

    for key in channels.keys():
        if bool(channels[key]):
            columns.append(key)

    verbose = False

    mode: int = int(config[SP][MODE])

    # Mode 1 is for Green, yellow orange and red only
    # Mode 0 is for Violet, Blue, Green and Yello only
    # Mode 2 continuously grab values of all colors
    if mode == 0:
        spectro.conversion_mode = spectro.MODE_0
    elif mode == 1:
        spectro.conversion_mode = spectro.MODE_1
    elif mode == 2:
        spectro.conversion_mode = spectro.MODE_2


    message = "Running "
    if run_MLX:
        message += "MLX Infrared Camera, "
    if run_MP:
        message += "MegaPixel Fisheye Camera, "
    if run_SP:
        message += "Infrared Spectrometer, "
    
    print(message)

    if verbose:
        print("MLX addr detected on I2C")
        print([hex(i) for i in mlx.serial_number])
        print(f"AS726x addr is {SPECTRO_ADDRESS} and GPIO is {SPECTRO_GPIO}")

    main(
        mlx,
        spectro,
        file_path = file_path, 
        run_mp = run_MP,
        run_mlx = run_MLX,
        run_sp = run_SP,
        columns = columns,
        verbose = verbose
    )

    print("Done")
