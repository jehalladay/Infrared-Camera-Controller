import time
import board
import busio
import numpy as np
import adafruit_mlx90640

# def matrixPrint(matrix:list):
#     for row in matrix:
#         for col in matrix[row]:
#             print(matrix[row][col], end="")
#         print()            
            
            
width = 32
height = 24
i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ

frame = [0] * 768 #Sets indexes to 0 this holds the IR readings
readings = [[0]*width]*height #This puts readings back into 2d matrix
numReadings = [[0]*width]*height #This puts readings back into 2d matrix

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
        start = end + 1
        end = start + 31
#         print(f"list {x} has: ", end="")
        print(numReadings[x], end="\n\n")
#     print(np.matrix(numReadings), end="\ndone\n")
#     print(np.matrix(readings), end="\nDone\n")
    #for h in range(24):
    #    for w in range(32,-1):
     #       t = frame[h * 32 + w]
     #   print()
    #time.sleep(3)
    