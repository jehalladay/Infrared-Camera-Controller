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
#These need to be hardcoded
K=np.array([[226.78774808876156, 0.0, 323.7695330830304], [0.0, 226.72792530533906, 218.94459567242427], [0.0, 0.0, 1.0]])
D=np.array([[-0.001113892387730428], [0.007489372244509825], [-0.019657948056696923], [0.0050755188856704755]])

file_name_ir = f'./data/{time.strftime("%Y_%m_%d")}_ir2.csv'
file_name_mp = f'./data/{time.strftime("%Y_%m_%d")}_mp.csv'

frm = 1

ir_frame = [0] * width * height
columns_ir = ['timestamp'] + [f'pixel_{i}' for i in range(width * height)]
column_mp = ['timestamp'] + [f'pixel_{i}' for i in range(640 * 480 * 3)]

create_csv(file_name_ir, columns_ir, True)
# create_csv(file_name_mp, column_mp, False)
while(1):
    stamp = time.monotonic()
    # cap = VideoCapture(0) #specify what USB to read from
    try: 
        # ret, mp_cap = cap.read()
        # while(ret is False):
        #     ret, mp_cap = cap.read()
            # time.sleep(0.2) #Give processor a break
        mlx.getFrame(ir_frame) #Capture frame from both cameras @ ~same_time
        #Configure ir_frame
        time.sleep(0.2) #Give processor a break
        if_frame = ['%.2f' % x for x in ir_frame]
        time.sleep(0.2) #Give processor a break
        start, end = 0, width
        for i in range(height):
            ir_frame[start:end] = ir_frame[start:end][::-1]
            start += width
            end += width
        time.sleep(0.2) #Give processor a break
        append_csv(file_name_ir, ir_frame, metadata = [stamp]) #Outputs IR camera data as an CSV
        time.sleep(0.2) #Give processor a break

        # mp_frame = mp_cap.reshape(-1)
        #Configure frame from mega_pixel
        # time.sleep(0.2) #Give processor a break
        # # append_csv(file_name_mp, mp_frame, metadata = [stamp]) #Outputs IR camera data as an CSV
        # imwrite(f"./data/{stamp}.jpg", mp_cap)
        # time.sleep(0.2) #Give processor a break
        # cap.release()
        # print(f"Completed Run: {frm}")
        # frm+=1
        time.sleep(3 - (time.monotonic() - stamp))
        print('\n\nRunning again\n')
    except ValueError:
        pass
