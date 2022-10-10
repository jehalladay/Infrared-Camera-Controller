import cv2
import numpy as np
import sys
import cv2
import glob

#Got help from supervisor at work to calibrate. Code is not going to be given
#These values Are the calibration values required to fix camera distortion
dimensions = (640, 480)
K=np.array([[226.78774808876156, 0.0, 323.7695330830304], [0.0, 226.72792530533906, 218.94459567242427], [0.0, 0.0, 1.0]])
D=np.array([[-0.001113892387730428], [0.007489372244509825], [-0.019657948056696923], [0.0050755188856704755]])

imageLocation = glob.glob('./largeSquares/*.jpg')
x = 0
for image in imageLocation:
    img = cv2.imread(image)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, dimensions, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imwrite(f"./calibrated/image{x+1}.jpg", undistorted_img)
    x = x+1