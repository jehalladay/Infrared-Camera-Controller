import time
import board
from adafruit_as726x import AS726x_I2C


max_val = 16000
max_graph = 500

def graph_map(x):
    return min(int(x*max_graph/ max_val), max_graph)

def console_write_graphically():
    print("\n")
    print("V: " + "="*graph_map((spectro.violet)))
    print("B: " + "="*graph_map((spectro.blue)))
    print("R: " + "="*graph_map((spectro.red)))
    print("Y: " + "="*graph_map((spectro.yellow)))
    print("G: " + "="*graph_map((spectro.green)))

def console_write_numerically():
    print("\n")
    print("V: " + str((spectro.raw_violet)))
    print("B: " + str((spectro.raw_blue)))
    print("R: " + str((spectro.raw_red)))
    print("Y: " + str((spectro.raw_yellow)))
    print("G: " + str((spectro.raw_green)))


i2c = board.I2C() #activates the RBPi default SCL and SDA pins
spectro = AS726x_I2C(i2c, 0x49) #Spectrometer address at 0x49

spectro.conversion_mode = spectro.MODE_2 #Continuously grab values of all colors
                                        #Mode 1 is for Green, yellow orange and red only
                                        #Mode 0 is for Violet, Blue, Green and Yello only

while(True):
    time.sleep(0.5)
    console_write_numerically()



