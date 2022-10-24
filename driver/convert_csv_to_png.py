'''
This file will take the pixel columns of a csv file and convert each row to a png image using a heatmap
'''

import os, sys, warnings
import numpy as np
import pandas as pd
import seaborn as sns
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

        # set up min and max values for picture scaling
        min = mean - scaling_factor * std
        max = mean + scaling_factor * std

        # remove these line later
        # min = mean - (std)
        # max = np.max(frame)
        
        # create the image
        fig, ax = plt.subplots()
        thermal = ax.imshow(np.zeros((height, width)), vmin = min, vmax = max)
        cbar = fig.colorbar(thermal)
        cbar.set_label('Temperature [$^{\circ}$C]', fontsize=14)
        
        #Below for Seaborn map, comment out above block!
        # ax = plt.subplots()
        # ax = sns.heatmap(frame, vmin = min, vmax =max, cmap='rocket') #Applying range rule of thumb from stat200

        #for thermal map
        thermal.set_data(frame)
        thermal.set_clim(vmin = min, vmax = max)
        ax.set_axis_off()

        # save the image
        img_name = f'frame_{i}'
        print(f'Converting row {i} to {output_dir}/{img_name}.png; min: {min}, max: {max}, mean: {mean}, std: {std}')
        #below for thermal
        fig.savefig(f'{output_dir}/{img_name}.png', dpi=300, facecolor='#FCFCFC', bbox_inches='tight')
        plt.close(fig)
        
        #this one for seaborn
        # plt.savefig(f'{output_dir}/{img_name}.png', dpi=300, facecolor='#FCFCFC', bbox_inches='tight')

if __name__ == "__main__":
    file_name = sys.argv[1]
    output_dir = sys.argv[2]
    scaling_factor = float(sys.argv[3])

    print(f'''
        Converting {file_name} to png images
        Output directory: {output_dir}
    ''')
    convert_csv_to_png(file_name, output_dir = output_dir, scaling_factor = scaling_factor)
