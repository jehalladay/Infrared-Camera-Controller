'''
This file will take the pixel columns of a csv file and convert each row to a png image using a heatmap
'''

import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def convert_csv_to_png(file_name: str, output_dir: str = 'output', width: int = 32, height: int = 24):
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

    for i in range(len(df)):
        row = df.iloc[i]
        pixels = np.array(row[pixel_columns]).reshape(height, width)

        fig, ax = plt.subplots()
        thermal = ax.imshow(np.zeros((height, width)), vmin = 0, vmax = 60)
        cbar = fig.colorbar(thermal)
        cbar.set_label('Temperature [$^{\circ}$C]', rotation=270)

        thermal.set_data(pixels)
        thermal.set_clim(vmin = np.min(pixels), vmax = np.max(pixels))

        ax.set_axis_off()
        img_name = f'frame_{i}.png'
        fig.savefig(f'{output_dir}/{img_name}.png', dpi=300, facecolor='#FCFCFC', bbox_inches='tight')
        plt.close(fig)


if __name__ == "__main__":
    file_name = sys.argv[1]
    output_dir = sys.argv[2]

    print(f'''
        Converting {file_name} to png images
        Output directory: {output_dir}
    ''')

    convert_csv_to_png(file_name, output_dir)
