#! /usr/bin/python3

import RPi.GPIO as GPIO  
import time
print("Running power output tests")
pinNumber = 29
GPIO.setmode(GPIO.BOARD) #Sets the type board type of numbers
GPIO.setup(pinNumber, GPIO.OUT)
counter = 0
GPIO.output(pinNumber, 1) #set output to high --> ON
while(1):
    GPIO.output(pinNumber, counter) #set output to high --> ON
    time.sleep(1)
    counter = (counter + 1)%2
