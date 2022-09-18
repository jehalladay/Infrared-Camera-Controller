'''
This file will take the pixel columns of a csv file and convert each row to a png image using a heatmap
'''

import os, sys, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

warnings.filterwarnings("ignore",category=cbook.mplDeprecation)

def convert_csv_to_png(file_name: str, output_dir: str = 'output', width: int = 32, height: int = 24, scaling_factor: int = 3):
    '''
        This function will convert the csv file to a series of png images
        Parameters:
            file_name: the name of the csv file
            output_dir: the name of the output directory
            width: the width of the pixels
            height: the height of the pixels
    '''
    df = pd.read_csv(file_name)
    pixel_columns = [f'pixel_{i}' for i in range(width * height)]

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # silence the MatplotlibDeprecationWarrning
    plt.rcParams.update({'figure.max_open_warning': 0})
    for i in range(len(df)):
        print(f'Converting row {i} to png')

        row = df.iloc[i] # grab next row
        pixels = np.array(row[pixel_columns]).reshape(height, width) # reshape into 2d array

        # rescale to 0-1 using the min and max of every frame so transitions are continuous
        min, max = np.min(df.values), np.max(df.values)
        pixels = (pixels - min) / (max - min)
        # raise the pixels to the power of the scaling factor to make the contrast between events higher
        pixels = pixels ** scaling_factor


        # create the image
        fig, ax = plt.subplots()
        thermal = ax.imshow(np.zeros((height, width)), vmin = 0, vmax = 60)
        cbar = fig.colorbar(thermal)
        thermal.set_data(pixels)
        thermal.set_clim(vmin = np.min(pixels), vmax = np.max(pixels))
        ax.set_axis_off()

        # save the image
        img_name = f'frame_{i}.png'
        fig.savefig(f'{output_dir}/{img_name}.png', dpi=300, facecolor='#FCFCFC', bbox_inches='tight')
        plt.close(fig)


if __name__ == "__main__":
    file_name = sys.argv[1]
    output_dir = sys.argv[2]
    scaling_factor = float(sys.argv[3])

    print(f'''
        Converting {file_name} to png images
        Output directory: {output_dir}
    ''')

    convert_csv_to_png(file_name, output_dir = output_dir, scaling_factor = scaling_factor)
