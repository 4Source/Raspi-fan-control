#!/usr/bin/python
#Version 0.6.0
import os
import time
import RPi.GPIO as GPIO
import logging
import argparse

TEMPERATURE_ON = 45
TEMPERATURE_OFF = 40

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename='/var/log/fancontrol.log', format=FORMAT, level=logging.INFO)

def getCPUtemperature():
    """Read out the cpu temperature"""
    res = os.popen('vcgencmd measure_temp').readline()
    temp = res.replace("temp=","").replace("'C\n","")
    return float(temp)

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Raspberry Pi Fan Control')

    # Add arguments
    parser.add_argument('--test', '-t', action='store_true', help='Test the fan is functional')

    # Parse arguments
    args = parser.parse_args()

    # Read temperature
    temp_float = getCPUtemperature()

    try:
        if args.test:
            print('Testing fan is functional!')
            print('Temperature: %s °C power on fan...', temp_float)
            GPIO.output(14, True)
            time.sleep(10)
            print('Temperature: %s °C power off fan...', temp_float)
            GPIO.output(14, False)
        # Turn on fan of above turn on threshold
        elif temp_float > TEMPERATURE_ON and GPIO.input(14) != True:
            logging.info('Temperature: %s °C power on fan...', temp_float)
            GPIO.output(14, True)
        # Turn off fan if below turn off threshold
        elif GPIO.input(14) != False and temp_float < TEMPERATURE_OFF:
            logging.info('Temperature: %s °C power off fan...', temp_float)
            GPIO.output(14, False)
        else:
            logging.info('Temperature: %s °C', temp_float)

    # If program is canceled turn off fan
    except KeyboardInterrupt:
        logging.info('Stopped by user...', float(getCPUtemperature()))
        if GPIO.input(14) != False:
            logging.info('Temperature: %s °C power off fan...', temp_float)
            GPIO.output(14, False)
        logging.info('Fan control stopped!')
        
if __name__ == "__main__":
    main()