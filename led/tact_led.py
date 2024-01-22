import init_fake_rpi
import RPi.GPIO as gpio
import time
from utils import print_rpi_versions

LED_PIN = 17
BUTTON_PIN = 26
MAX_PRESSED = 5


def setup():
    print(f"Press the button {MAX_PRESSED} times")
    gpio.setmode(gpio.BCM)
    gpio.setup(LED_PIN, gpio.OUT)
    gpio.setup(BUTTON_PIN, gpio.IN)


print_rpi_versions()
setup()

counter = 0
prev_value = gpio.LOW

while counter < MAX_PRESSED * 2:
    value = gpio.input(BUTTON_PIN)
    if prev_value != value:
        prev_value = value
        counter += 1
        if counter % 2 == 0:
            times = int(counter / 2)
            print(f"Button pressed: {times}")

    if value == gpio.HIGH:
        gpio.output(LED_PIN, gpio.HIGH)
    else:
        gpio.output(LED_PIN, gpio.LOW)
    time.sleep(0.1)

gpio.cleanup()
