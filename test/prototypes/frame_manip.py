import time

import pandas as pd
import numpy as np

# from cv2 import (
#     # VideoCapture,
#     imwrite
# )

# load frame.csv to dataframe
df = pd.read_csv("frame.csv", header = None)

print(df.values.shape)

arr = df.values.reshape(480, 640, 3)

print(arr.shape)

print(time.strftime("%Y_%m_%d"))

# imwrite("frame.jpg", arr)