import time
import board
import busio
import numpy as np
from datetime import date
import adafruit_mlx90640
            
width = 32
height = 24
i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])


def create_csv(file_name: str, width: int = 32, height: int = 24):
    '''
        This function will check to see if a csv file exists
        If it does not exist, it will create the file
        If it does exist, it will do nothing
    '''
    try:
        with open(file_name, 'r') as f:
            pass
    except FileNotFoundError:
        print(f"Creating new file {file_name}\n")
        with open(file_name, 'w') as f:
            f.write(','.join([f'pixel_{i}' for i in range(width * height)]))
            

def append_csv(file_name: str, data: list):
    '''
        This function will append the data to the csv file
    '''
    with open(file_name, 'a') as f:
        f.write('\n' + ','.join([str(i) for i in data]))

def scan_and_flip(file_name: str, width: int = 32, height: int = 24):
    '''
        This function will scan the MLX90640 and flip the data
        The data will be appended to the csv file
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
        print(f"print@ {stamp}\n{frame}\n\n")
        append_csv(file_name, frame)
    except ValueError:
        pass


def new_main(file_name: str = './readingsCSV/test.csv', width: int = 32, height: int = 24):

    create_csv(file_name, width = width, height = height)

    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ

    while True:
        stamp = time.monotonic()
        scan_and_flip(file_name, width = width, height = height)
        print(f"Writing at {stamp}")
        time.sleep(1 - (time.monotonic() - stamp))


#Leaving here for testing
def old_main():

    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ

    frame = [0] * 768 #Sets indexes to 0 this holds the IR readings     
    readings = [[0]*width]*height #This puts readings back into 2d matrix    <---- One of these will be made obselete
    numReadings = [[0]*width]*height #This puts readings back into 2d matrix <---- One of these will be made obselete
    frameRow = list()

    while True:
        stamp = time.monotonic()
        try:
            mlx.getFrame(frame)
        except ValueError:#if read failed, try again w/o delay
            continue
        start, end = 0, 31
        formatedFrame = ['%.2f' % x for x in frame]
        for i in range(0, 24): #reverse slices of the frame by rows
            formatedFrame[start:end] = formatedFrame[start:end][::-1] # <----- is there a way to cast and flip rows?
            start = start+32
            end = end+32
        today = date.today()
        print(f"Writing at time: {stamp}\n{formatedFrame}\n")
        np.savetxt(f"./readingsCSV/{today}.csv", formatedFrame, delimiter=", ", fmt='% s')
        time.sleep(3 - (time.monotonic() - stamp)) #Wait 3 seconds from read


if __name__ == '__main__':
    # choose whether to use old main or new main based on command line argument
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'old':
        old_main()
    elif len(sys.argv) > 3:
        file_name = sys.argv[1] 
        width = int(sys.argv[2])
        height = int(sys.argv[3])
        new_main(file_name=file_name, width = width, height=height)
    else:
        new_main()
