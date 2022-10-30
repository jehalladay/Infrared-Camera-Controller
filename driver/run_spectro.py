import sys
import time
import board

from adafruit_as726x import AS726x_I2C
from AS.readSpectro import(readSpectro)
from utils.csv_handling import (
    append_csv,
    create_csv
)

spectro_address = 0x49
spectro_GPIO = 21

def main(file_name: str = "./readingsCSV/spectro_test.csv", verbose: bool = False):
    frame = ['violet','blue', 'green', 'yellow', 'orange', 'red']
    create_csv(file_name, 
        columns = frame,
        verbose = verbose 
    )
    while(True):
        frame = readSpectro(spectro, True)
        append_csv(file_name=file_name, data=frame)
        time.sleep(3) #This should be dynamic from JSON

if __name__ == '__main__':
    print(f"AS726x addr is {spectro_address}")
    i2c = board.I2C() #activates the RBPi default SCL and SDA pins
    spectro = AS726x_I2C(i2c, 0x49) #Spectrometer address at 0x49
    spectro.conversion_mode = spectro.MODE_2 #Continuously grab values of all colors
                                             #Mode 1 is for Green, yellow orange and red only
                                             #Mode 0 is for Violet, Blue, Green and Yello only

    date = time.strftime("%Y_%m_%d") # get todays date
    file_name = f'./readingsCSV/spectrometer{date}.csv'
    verbose = False

    if len(sys.argv) > 1:
        file_name = sys.argv[1] 
    if len(sys.argv) > 2:
        verbose = bool(int(sys.argv[2]))

    main(
        file_name = file_name,  
        verbose = verbose
    )

