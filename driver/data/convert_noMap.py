'''
This file will take the pixel columns of a csv file and convert each row to a png image using a heatmap
'''

import os, sys, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

warnings.filterwarnings("ignore",category=cbook.mplDeprecation)
def convert_csv_to_png(
    file_name: str, 
    output_dir: str = 'output', 
    width: int = 32, 
    height: int = 24,
    scaling_factor: int = 3,
):
    '''
        This function will convert the csv file to a series of png images
        Parameters:
            file_name: the name of the csv file
            output_dir: the name of the output directory
            width: the width of the frame
            height: the height of the frame
            scaling_factor: the number of standard deviations from the mean to include in the heatmap
    '''

    df = pd.read_csv(file_name)
    pixel_columns = [f'pixel_{i}' for i in range(width * height)]

    # create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for i in range(len(df)):
        # grab the next row
        row = df.iloc[i]

        # reshape into 2d array
        frame = np.array(row[pixel_columns]).reshape(height, width) 
        frame[8][2] = (frame[7][2] + frame[9][2] + frame[8][1] + frame[8][3]) / 4
        # grab statistical data on the frame
        std, mean = np.std(frame), np.mean(frame)
        for i in frame:
            print(i)
        # set up min and max values for picture scaling
        min = mean - scaling_factor * std
        max = mean + scaling_factor * std
        
        # create the image
        fig, ax = plt.subplots()
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())

        thermal = ax.imshow(np.zeros((height, width)), vmin = min, vmax = max)
        thermal.set_data(frame)

        img_name = f'frame_0'
        print(f'Converting row {i} to {output_dir}/{img_name}.png; min: {min}, max: {max}, mean: {mean}, std: {std}')
        plt.margins(0,0)
        plt.gca().set_axis_off()
        fig.savefig(f'{output_dir}/{img_name}.png', dpi=35, facecolor='#FCFCFC', bbox_inches='tight', pad_inches = 0)
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
