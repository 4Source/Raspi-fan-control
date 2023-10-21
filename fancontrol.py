#!/usr/bin/python
#Version 0.5.0
import os
import time
import RPi.GPIO as GPIO
import logging
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename='/var/log/fan-info.log', format=FORMAT, level=logging.INFO)

#funktion: Temperatur mit Hilfe von vcgencmd auslesen und als Text zurueckliefern
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Temperatur lesen und in einen Float wandeln
temp_float = float(getCPUtemperature())

try:
    # temperatur > 45, dann Luefter an
    if temp_float > 45 and GPIO.input(14) != True:
        logging.info('%s °C power on fan...', temp_float)
        # ein
        GPIO.output(14, True)
    elif GPIO.input(14) != False:
        logging.info('%s °C power off fan...', temp_float)
        # aus
        GPIO.output(14, False)
    # nothing changed

# Wird das Programm abgebrochen, dann den Luefter wieder ausschalten
except KeyboardInterrupt:
    logging.warn('%s °C power off fan. Stopped by User! Cancelling...', float(getCPUtemperature()))
    GPIO.output(14, False)
