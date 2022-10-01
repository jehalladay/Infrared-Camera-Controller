'''
    File contains utility functions that are used by other files
'''

def create_csv(file_name: str, columns: list = [], verbose: bool = False):
    '''
        This function will check to see if a csv file exists
        If it does not exist, it will create the file
        If it does exist, it will do nothing
    '''

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
        sample = data + metadata
        f.write('\n' + ','.join([str(i) for i in sample]))
