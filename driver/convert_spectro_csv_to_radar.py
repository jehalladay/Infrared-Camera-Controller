'''
This file will take the pixel columns of a csv file and convert each row to a png image using a heatmap
'''

import json, os, sys, warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

from utils.constants import (
    RADAR_CONFIG_JSON,
    COLOR_CHANNELS
)

warnings.filterwarnings("ignore",category=cbook.mplDeprecation)
def convert_from_csv_to_radar(
    file_name: str, 
    output_dir: str = 'output', 
    columns: list = ['violet', 'red', 'green', 'blue', 'orange', 'yellow', 'temperature']
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
    columns = [col for col in columns if col in df.columns]

    categories = [*columns, columns[0]]

    # create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for i in range(len(df)):

        # grab the next row
        row = df.iloc[i]

        if 'timestamp' in df.columns:
            timestamp = str(row['timestamp'])
        else:
            timestamp = str(i)
        
        data = [*row[columns].to_list(), row[columns].to_list()[0]]

        label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(data))


        plt.figure(figsize=(8, 8))
        plt.subplot(polar=True)
        plt.plot(label_loc, data, label=f'')
        plt.title(f'Spectral Radar for {timestamp}', size=20, y=1.05)
        lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
        plt.legend()
        img_name = f'spectral_radar_{timestamp}.png'
        
        plt.savefig(f'{output_dir}/{img_name}.png')
        plt.clf()


if __name__ == "__main__":
    file_name = sys.argv[1]
    output_dir = sys.argv[2]

    # get config file 

    config: dict = json.load(open(RADAR_CONFIG_JSON, 'r'))
    channels: dict = config[COLOR_CHANNELS]

    columns = []

    for key in channels.keys():
        if bool(channels[key]):
            columns.append(key)


    print(f'''
        Converting {file_name} to png images
        Output directory: {output_dir}
    ''')

    convert_from_csv_to_radar(
        file_name, 
        output_dir = output_dir, 
        columns = columns
    )
