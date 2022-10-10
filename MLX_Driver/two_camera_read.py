import sys, time
import board
import busio
import adafruit_mlx90640
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
mlx = adafruit_mlx90640.MLX90640(i2c)
width: int = 32
height: int = 24
dimensions = (640, 480)
#These need to be hardcoded
K=np.array([[226.78774808876156, 0.0, 323.7695330830304], [0.0, 226.72792530533906, 218.94459567242427], [0.0, 0.0, 1.0]])
D=np.array([[-0.001113892387730428], [0.007489372244509825], [-0.019657948056696923], [0.0050755188856704755]])

frm = 1
ir_frame = [0] * width * height
while(frm < 10):
    stamp = time.monotonic()
    cap = cv2.VideoCapture(0) #specify what USB to read from
    try: 
        ret, mp_frame = cap.read()
        while(ret is False):
            ret, mp_frame = cap.read()
            time.sleep(0.1) #Give processor a break

        mlx.getFrame(ir_frame) #Capture frame from both cameras @ ~same_time
        #Configure ir_frame
        if_frame = ['%.2f' % x for x in ir_frame]
        start, end = 0, width
        for i in range(height):
            ir_frame[start:end] = ir_frame[start:end][::-1]
            start += width
            end += width
        time.sleep(0.2) #Give processor a break
        #Configure frame from mega_pixel
        cv2.imwrite(f"./megaPixel-Camera/{frm}_mp.jpg", undistorted_img)
        cap.release()
        frm += 1
        time.sleep(3 - (time.monotonic - stamp))
           
    except ValueError:
        pass
    time.sleep(3)
