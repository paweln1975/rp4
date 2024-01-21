import init_fake_rpi
import RPi.GPIO as gpio
import time
from utils import print_rpi_versions

LED_PIN = 17


def setup():
    gpio.setmode(gpio.BCM)
    gpio.setup(LED_PIN, gpio.OUT)


setup()
print_rpi_versions()

gpio.output(LED_PIN, gpio.HIGH)
time.sleep(3)
gpio.output(LED_PIN, gpio.LOW)

gpio.cleanup()

