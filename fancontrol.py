#!/usr/bin/python
#Version 0.6.0
import os
import time
import RPi.GPIO as GPIO
import logging

TEMPERATURE_ON = 45
TEMPERATURE_OFF = 40

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename='/var/log/fan-info.log', format=FORMAT, level=logging.INFO)

def getCPUtemperature():
    """Read out the cpu temperature"""
    res = os.popen('vcgencmd measure_temp').readline()
    temp = res.replace("temp=","").replace("'C\n","")
    return float(temp)

# Read temperature
temp_float = getCPUtemperature()

try:
    # Turn on fan of above turn on threshold
    if temp_float > TEMPERATURE_ON and GPIO.input(14) != True:
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
    