'''
    Inrared Camera Controller
    File: generate.py
    Description: This program will generate dummy data for the csv to photo pipeline
    Software Engineering
    Date: 9/13/2022


    *******************************************************************************
        We generate a csv file with the following schema:
        1. Row ID: integer
        2. Timestamp: timestamp
        3-770. 768 pixel values: float
        771-780. operation flags: binary

        Core assumptions for data generation:
            The values that populate the CSV are random
            every timestamp is later than the timestamp of the row ids before it

    *******************************************************************************
'''


import sys, time
import numpy as np
import pandas as pd




def generate_data(file_name: str, rows: int, delta: int = 10, flags: int = 10, pixel_width: int = 32, pixel_height: int = 24):
    '''
        This function will generate the dummy data for the csv to photo pipeline
        Parameters:
            file_name: the name of the file to be generated
            rows: the number of rows to be generated
    '''

    row_ids = np.arange(rows)
    timestamps = np.array([time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + i * delta * 60)) for i in range(rows)])
    pixel_values = np.random.rand(rows, pixel_width * pixel_height)
    operation_flags = np.random.randint(2, size=(rows, flags))

    columns = ['row_id', 'timestamp'] + [f'pixel_{i}' for i in range(pixel_width * pixel_height)] + [f'operation_flag_{i}' for i in range(flags)]

    df = pd.DataFrame(np.concatenate((row_ids.reshape(-1, 1), timestamps.reshape(-1, 1), pixel_values, operation_flags), axis=1), columns=columns)

    df.to_csv(file_name, index=False)




if __name__ == "__main__":
    file_name = sys.argv[1]
    rows = int(sys.argv[2])

    delta = 10
    flags = 10
    pixels = (32, 24)
    
    print(f'''
        Generating {rows} rows of data
        File name: {file_name}
        Time delta: {delta} minutes
        Operation flags: {flags}
        Pixel dimensions: {pixels[0]} x {pixels[1]}
    ''')

    generate_data(
        file_name, 
        rows,
        delta = delta,
        flags = flags,
        pixel_width = pixels[0],
        pixel_height = pixels[1]
    )