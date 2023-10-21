#!/usr/bin/python
import os
import time
import RPi.GPIO as GPIO
import logging
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
logging.basicConfig(filename='fancontrol.log', format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)

#funktion: Temperatur mit Hilfe von vcgencmd auslesen und als Text zurueckliefern
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Temperatur lesen und in einen Float wandeln
temp_float = float(getCPUtemperature())

try:
    # temperatur > 47, dann Luefter an
    if (temp_float > 47):
        logging.info('%s power on fan...', temp_float)
        # ein
        GPIO.output(14, True)
    else:
        logging.info('%s power off fan...', temp_float)
        # aus
	GPIO.output(14, False)


# Wird das Programm abgebrochen, dann den Luefter wieder ausschalten
except KeyboardInterrupt:
    print(float(getCPUtemperature()))
    print("power off fan...")
    GPIO.output(14, False)
    print("cancelling...")
