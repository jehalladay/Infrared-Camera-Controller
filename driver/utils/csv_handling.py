'''
    File contains utility functions that are used by other files
'''

from pathlib import (
    Path
)

from .types import (
    Frame,
    Metadata,
    Picture
)

def create_csv(file_name: str, columns: list = [], verbose: bool = False):
    '''
        This function will check to see if a csv file exists
        If it does not exist, it will create the file
        If it does exist, it will do nothing
    '''

    if not Path(file_name).exists():
        if verbose:
            print(f"Creating {Path(file_name).parent} directory(s)")
        Path(file_name).parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(file_name, 'r') as f:
            pass

    except FileNotFoundError:
        if verbose:
            print(f"Creating new file {file_name}\n")

        with open(file_name, 'w') as f:
            f.write(','.join(columns))
            

def append_csv(file_name: str, data: list, metadata: list = []):
    '''
        This function will append the data to the csv file
    '''

    with open(file_name, 'a') as f:
        sample = metadata + data
        f.write('\n' + ','.join([str(i) for i in sample]))
