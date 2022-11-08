import sys, time
import board
import busio
import adafruit_mlx90640
import numpy as np
from cv2 import(
    VideoCapture,
    imwrite
)
from utility import (
    create_csv,
    append_csv
)
from PIL import Image


i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ

width: int = 32
height: int = 24
dimensions = (640, 480)

file_name_ir = f'./data/{time.strftime("%Y_%m_%d")}_ir2.csv'
file_name_mp = f'./data/{time.strftime("%Y_%m_%d")}_mp.csv'
frm = 1

ir_frame = [0] * width * height
columns_ir = ['timestamp'] + [f'pixel_{i}' for i in range(width * height)]

create_csv(file_name_ir, columns_ir, True)
create_csv(file_name_mp, column_mp, False)
while(1):
    stamp = time.monotonic()
    cap = VideoCapture(0) #specify what USB to read from
    try: 
        ret, mp_cap = cap.read()
        while(ret is False):
            ret, mp_cap = cap.read()
            time.sleep(0.2) #Give processor a break
        mlx.getFrame(ir_frame) #Capture frame from both cameras @ ~same_time
        #Configure ir_frame
        time.sleep(0.2) #Give processor a break
        if_frame = ['%.2f' % x for x in ir_frame]
        time.sleep(0.2) #Give processor a break
        #The next 5 lines should be deleted once the camera flipping is implemented in convert_csv**.py 
        start, end = 0, width
        for i in range(height):
            ir_frame[start:end] = ir_frame[start:end][::-1]
            start += width
            end += width
        time.sleep(0.2) #Give processor a break
        append_csv(file_name_ir, ir_frame, metadata = [stamp]) #Outputs IR camera data as an CSV
        time.sleep(0.2) #Give processor a break

        #Configure frame from mega_pixel
        time.sleep(0.2) #Give processor a break
        append_csv(file_name_mp, mp_frame, metadata = [stamp]) #Outputs IR camera data as an CSV
        imwrite(f"./data/{stamp}.jpg", mp_cap)
        time.sleep(0.2) #Give processor a break
        cap.release()
        frm+=1
        print(f'\n\nRunning frame: {frm+1} in 3 seconds\n')#Keep this while testing
        time.sleep(3 - (time.monotonic() - stamp))
    except ValueError:
        pass
