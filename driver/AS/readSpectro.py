def readSpectro(
    spectro, 
    verbose: bool = False, 
    columns: list = ['violet', 'blue', 'green', 'yellow', 'orange', 'red']
) -> list:
    '''
        This function will return an array with the desired readings from the spectrometer
    '''

    frame = []
    message: str = "Frame: "

    for col in columns:
        if hasattr(spectro, col):
            frame.append(getattr(spectro, col))
            message += f"{col}: {getattr(spectro, col)}; "
    
    if verbose:
        print(message)

    return frame
