import RPi.GPIO as GPIO
import time
from importlib.metadata import version

LED_PIN = 17

def print_RP_versions():
    print("RPi.GPIO version: {}".format(version('RPi.GPIO')))
    
    info = GPIO.RPI_INFO
    print("P1_REVISION: {}".format(info['P1_REVISION']))
    print("REVISION: {}".format(info['REVISION']))
    print("TYPE: {}".format(info['TYPE']))
    print("MANUFACTURER: {}".format(info['MANUFACTURER']))
    print("PROCESSOR version: {}".format(info['PROCESSOR']))
    print("RAM: {}".format(info['RAM']))
    

GPIO.setmode(GPIO.BCM)
print_RP_versions()
GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.output(LED_PIN, GPIO.HIGH)
time.sleep(1)
GPIO.output(LED_PIN, GPIO.LOW)
time.sleep(1)

GPIO.cleanup()

