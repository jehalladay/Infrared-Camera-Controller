'''
This file will take two images of the same region of space and compose them by overlaying their common features.
'''

import json, os, sys, time, warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

from PIL import Image

from utils.constants import (
    ALPHA,
    COMPOSE_CONFIG_JSON,
    DATE_FORMAT,
    PATH,
    PLACEMENT,
    SCALING_FACTOR,
    SIZE,
    STORAGE,
    WIDTH,
    HEIGHT,
    X,
    Y
)

warnings.filterwarnings("ignore",category=cbook.mplDeprecation)

def compose_images(
    bottom_image_file: str, 
    top_image_file: str, 
    output_dir: str = 'output',
    top_original_size: tuple = (32, 24),
    top_alpha_value: int = 150,
    placment_of_top_left_of_bottom_image: tuple = (270, 210),
):
    '''
        This function will take two pictures, with the bottom picture being from the megapixel and the top picture being the infrared camera,
            and compose them into one image. The resulting image should have the pictures accurately overlayed on top of each other.
        Parameters:
            bottom_image_file: the name of the image file
            top_image_file: the name of the image file
            output_dir: the place to save the output image

        Check out:
            https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv#comment63502914_14102014 for offsetting
            https://imagekit.io/blog/image-resizing-in-python/ for padding
            https://pythonexamples.org/python-opencv-add-blend-two-images/ for blending
            https://www.geeksforgeeks.org/python-pil-image-resize-method/ for resizing
    '''

    bottom = Image.open(bottom_image_file)
    top = Image.open(top_image_file)

    # resize the top image to the size of the bottom image
    top = top.resize(top_original_size, Image.ANTIALIAS)
    top.putalpha(top_alpha_value)

    bottom.paste(top, placment_of_top_left_of_bottom_image, mask = top)

    # strip old file names of their extensions to make new name
    file_name: str = f'{bottom_image_file.split(".")[0]}_{top_image_file.split(".")[0]}_composed.png'


    # save the image
    bottom.save(os.path.join(output_dir, file_name))

    
if __name__ == "__main__":
    bottom_image_file: str = sys.argv[1]
    top_image_file: str = sys.argv[2]

    # get todays date
    date = time.strftime(DATE_FORMAT)

    config: dict = json.load(open(COMPOSE_CONFIG_JSON, 'r'))
    output_dir: str = config[STORAGE][PATH].format(conversion_date = date)
    top_original_size: tuple = (
        int(config[SIZE][WIDTH]),
        int(config[SIZE][HEIGHT])
    )
    
    top_alpha_value: int = int(config[ALPHA])
    placment_of_top_left_of_bottom_image: tuple = (
        int(config[PLACEMENT][X]),
        int(config[PLACEMENT][Y])
    )

    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    if len(sys.argv) > 3:
        scaling_factor = float(sys.argv[3])

    print(f'''
        Composing the images: {bottom_image_file} and {top_image_file} into a single image
        Output directory: {output_dir}
    ''')

    compose_images(
        bottom_image_file,
        top_image_file, 
        output_dir = output_dir,
        top_original_size = top_original_size,
        top_alpha_value = top_alpha_value,
        placment_of_top_left_of_bottom_image = placment_of_top_left_of_bottom_image,
    )

    print('Done!')

