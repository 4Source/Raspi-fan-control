#!/usr/bin/python
import os
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)

#funktion: Temperatur mit Hilfe von vcgencmd auslesen und als Text zurueckliefern
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Temperatur lesen und in einen Float wandeln
temp_float = float(getCPUtemperature())

try:
    # temperatur > 47, dann Luefter an
    if (temp_float > 47):
        print(temp_float)
        print("power on fan...")
        # ein
        GPIO.output(14, True)
        # und jetzt 58 Sekunden laufen lassen. (Das passt dann gut mit dem Minuten Timer)
        time.sleep(58)
        print("power off fan...")
        # aus
        GPIO.output(14, False)
        print(float(getCPUtemperature()))
    else:
        print(temp_float)
        print("temp low")

# Wird das Programm abgebrochen, dann den Luefter wieder ausschalten
except KeyboardInterrupt:
    print(float(getCPUtemperature()))
    print("power off fan...")
    GPIO.output(14, False)
    print("cancelling...")
