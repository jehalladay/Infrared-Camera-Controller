def readSpectro(spectro, verbose: bool = False):
    #               0                   1                   2                   3                   4                   5           
    frame = [spectro.raw_violet, spectro.raw_blue, spectro.raw_green, speectro.raw_yellow, spectro.raw_orange, spectro.raw_red]
    if verbose:
        print("Violet: " + str((frame[0])))
        print("Blue  : " + str((frame[1])))
        print("Green : " + str((frame[2])))
        print("Yellow: " + str((frame[3])))
        print("Orange: " + str((frame[4])))
        print("Red   : " + str((frame[5])))
    return frame
