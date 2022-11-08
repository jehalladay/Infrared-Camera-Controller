import board, json, sys, time

from adafruit_as726x import (
    AS726x_I2C
)

from AS.readSpectro import (
    readSpectro
)

from utils.csv_handling import (
    append_csv,
    create_csv
)

from utils.constants import (
    COLOR_CHANNELS,
    DATE_FORMAT,
    TIME_FORMAT,
    DURATION,
    FREQUENCY,
    LOCATION,
    MODE,
    PATH,
    PRECISION,
    RECORDING,
    STORAGE,
    SPECTRO_CONFIG_JSON,
    SPECTRO_ADDRESS,
    SPECTRO_GPIO
)


def main(
    spectro,
    file_name: str = "./readingsCSV/spectro_test.csv", 
    precision: int  = 2,
    duration : int  = 20,
    frequency: int  = .1,
    columns  : list = ['violet', 'blue', 'green', 'yellow', 'orange', 'red'],
    verbose: bool = False
) -> None:
    '''
        This function will control the loop for operating the spectrometer
    '''

    frame      : list = []
    csv_columns: list = ['timestamp'] + columns

    create_csv(
        file_name, 
        columns = csv_columns,
        verbose = verbose 
    )

    # while(True):
    while duration > 0:
        stamp = time.monotonic()


        if verbose:
            print(f"Reading at {time.monotonic()}")

        frame = readSpectro(
            spectro, 
            True, 
            columns = columns
        )
        
        append_csv(
            file_name = file_name, 
            data      = frame, 
            metadata  = [stamp]
        )

        duration -= frequency
        time.sleep(frequency)


if __name__ == '__main__':
    # activate the RBPi default SCL and SDA pins
    i2c = board.I2C()

    # Spectrometer address at 0x49, set inside utils/constants.py
    spectro = AS726x_I2C(i2c, SPECTRO_ADDRESS) 

    # get todays date
    date = time.strftime(DATE_FORMAT)
    timestamp = time.strftime(TIME_FORMAT)

    # load config from ./config/spectro.json
    config: dict = json.load(open(SPECTRO_CONFIG_JSON, 'r'))

    file_path = config[STORAGE][PATH]
    file_name = file_path + config[STORAGE][LOCATION]
    
    file_name = file_name.format(
        date = date, 
        time = timestamp
    )

    precision = int(config[STORAGE][PRECISION])
    duration  = float(config[RECORDING][DURATION])
    frequency = float(config[RECORDING][FREQUENCY])

    channels: dict = config[COLOR_CHANNELS]

    columns = []

    for key in channels.keys():
        if channels[key]:
            columns.append(key)

    verbose = False

    mode: int = int(config[MODE])

    # Mode 1 is for Green, yellow orange and red only
    # Mode 0 is for Violet, Blue, Green and Yello only
    # Mode 2 continuously grab values of all colors
    if mode == 0:
        spectro.conversion_mode = spectro.MODE_0
    elif mode == 1:
        spectro.conversion_mode = spectro.MODE_1
    elif mode == 2:
        spectro.conversion_mode = spectro.MODE_2


    if len(sys.argv) > 1:
        file_name = sys.argv[1] 
    if len(sys.argv) > 2:
        verbose = bool(int(sys.argv[2]))

    print(f"Running Spectrometer for {duration} seconds at {1/frequency} Hz")

    if verbose:
        print(f"AS726x addr is {SPECTRO_ADDRESS} and GPIO is {SPECTRO_GPIO}")

    main(
        spectro,
        file_name = file_name,
        columns   = columns,
        precision = precision,
        verbose   = verbose
    )

    print("Spectrometer: Done")
