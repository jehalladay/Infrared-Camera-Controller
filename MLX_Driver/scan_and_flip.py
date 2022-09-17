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

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ

frame = [0] * 768 #Sets indexes to 0 this holds the IR readings     
readings = [[0]*width]*height #This puts readings back into 2d matrix    <---- One of these will be made obselete
numReadings = [[0]*width]*height #This puts readings back into 2d matrix <---- One of these will be made obselete
frameRow = list

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
