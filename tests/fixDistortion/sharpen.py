import cv2
import numpy as np

image = cv2.imread('capture_3.jpg')
cv2.waitKey()
cv2.destroyAllWindows()
cv2.imshow('Current Image', image)

kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
image_sharp = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
cv2.imshow('Sharpened image', image_sharp)
cv2.imshow('Current Image', image)
cv2.waitKey() == 'q'
cv2.destroyAllWindows()