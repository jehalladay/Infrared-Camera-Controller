from cv2 import (
    imwrite
)

def save_image(image, file_name):
    imwrite(file_name, image)