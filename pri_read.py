import init_fake_rpi
import RPi.GPIO as gpio
import time
from utils import print_rpi_versions

PIR_PIN = 4
BUTTON_PIN = 26


def setup():
    gpio.setmode(gpio.BCM)
    gpio.setup(PIR_PIN, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    gpio.setup(BUTTON_PIN, gpio.IN)


setup()
print_rpi_versions()

tact_status = gpio.LOW

try:
    while tact_status == gpio.LOW:
        time.sleep(0.1)
        movement_detected = gpio.input(PIR_PIN)
        if movement_detected:
            print("Movement detected        ", end="\r")
        else:
            print("Movement NOT detected    ", end="\r")
        tact_status = gpio.input(BUTTON_PIN)
except KeyboardInterrupt:
    pass

gpio.cleanup()
