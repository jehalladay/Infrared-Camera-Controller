'''
This program will take a sample number and check the csv file to see its length 
    and print off the last 10 columns of the sample
'''

import sys
import pandas as pd
import numpy as np

def check_csv(file_name: str, sample_number: int):
    '''
        This function will check the csv file and print off the last 10 columns of the sample
        Parameters:
            file_name: the name of the csv file
            sample_number: the sample number to check
    '''
    df = pd.read_csv(file_name)
    sample_number += 1
    pixel_columns = [f'pixel_{i}' for i in range(len(df.iloc[sample_number]))]
    print(f'Length of csv file: {len(df)}')
    print(f'Length of sample {sample_number - 1}: {len(df.iloc[sample_number])}')
    print(df[pixel_columns].iloc[sample_number])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        row = int(sys.argv[1])
        check_csv('../MLX_Driver/readingsCSV/test7.csv', row)
    else:
        check_csv('../MLX_Driver/readingsCSV/test7.csv', 130)