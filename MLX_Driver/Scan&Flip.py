import time
import board
import busio
import numpy as np
import adafruit_mlx90640
import csv
            
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
    formatedFrame = ['%.2f' % x for x in frame]
    start,end = 0, 31
    for x in range(0, 24): #Try using myList[start:end:step]
        numReadings[x] = formatedFrame[end:start:-1] #Need IR scanner flips the image aroundy-axis, this is to un-flip it
        frameRow = formatedFrame[end:start:-1]
        start = end + 1
        end = start + 31
#         print(f"list {x} has: ", end="")
        print("numReadings\n",numReadings[x], end="\n\n")
        print(f"frameRow {x}:\n", frameRow, end="\n\n")
        for i in range (0, 31):
            if frameRow[i] != numReadings[x][i]:
                printf(f"Error difference in readings: in frameRow: {frameRow[i]} in numReadings[x]: {numReadings[x][i]}\n")
                quit()
#      with open(f"{stamp}.csv", 'w') as file:
#         write = csv.writer(file)
#         write.writerows(frameRow)
    np.savetxt(f"readingsCSV/{stamp}.csv", frameRow, delimiter=", ", fmt='% s')
    time.sleep(3 - (time.monotonic() - stamp)) #Wait 3 seconds from read

    