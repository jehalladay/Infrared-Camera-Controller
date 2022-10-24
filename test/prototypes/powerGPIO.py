#!/usr/bin/python3

#use to check power usage of additional i2c device
import RPi.GPIO as GPIO  
import time
print("Running power output tests")
pinNumber = 18
GPIO.setmode(GPIO.BOARD) #Sets the type board type of numbers
GPIO.setup(29, GPIO.OUT)
counter = 0
while(1):
    GPIO.output(29, counter%2) #set output to high
    time.sleep(0.5)
    counter+=1
