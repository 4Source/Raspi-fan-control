#!/usr/bin/python
#Version 0.6.0
import os
import time
import RPi.GPIO as GPIO
import argparse

TEMPERATURE_ON = 60
TEMPERATURE_OFF = 45

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)

def getCPUtemperature():
    """Read out the cpu temperature"""
    res = os.popen('vcgencmd measure_temp').readline()
    temp = res.replace("temp=","").replace("'C\n","")
    return temp

def main():
    try:
            
        # Create argument parser
        parser = argparse.ArgumentParser(description='Raspberry Pi Fan Control')

        # Add arguments
        parser.add_argument('--test', '-t', action='store_true', help='Test the fan is functional')

        # Parse arguments
        args = parser.parse_args()

        # Read temperature
        temp = getCPUtemperature()
        temp_float = float(temp)

        if args.test:
            print('Testing fan is functional!')
            print(f'Temperature: {temp} °C power on fan...')
            GPIO.output(14, True)
            time.sleep(10)
            print(f'Temperature: {temp} °C power off fan...')
            GPIO.output(14, False)
        # Turn on fan of above turn on threshold
        elif temp_float > TEMPERATURE_ON and GPIO.input(14) != True:
            print(f'Temperature: {temp} °C power on fan...')
            GPIO.output(14, True)
        # Turn off fan if below turn off threshold
        elif GPIO.input(14) != False and temp_float < TEMPERATURE_OFF:
            print(f'Temperature: {temp} °C power off fan...')
            GPIO.output(14, False)
        else:
            print(f'Temperature: {temp} °C')

    # If program is canceled turn off fan
    except KeyboardInterrupt:
        print('Stopped by user...')
        if GPIO.input(14) != False:
            print(f'Temperature: {temp} °C power off fan...')
            GPIO.output(14, False)
        print('Fan control stopped!')
        exit(0)
        
if __name__ == "__main__":
    main()
    exit(0)