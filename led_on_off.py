import init_fake_rpi
import RPi.GPIO as gpio
import time
from utils import print_rpi_versions

LED_1_PIN = 17
LED_2_PIN = 27
LED_3_PIN = 22

led_list = [LED_1_PIN, LED_2_PIN, LED_3_PIN]


def power_on_off_led(index: int, state: int):
    if index not in led_list:
        print(f"Invalid GPIO index value. It should be one of {led_list}")

    if state == 0 or state == 1:
        if state == 0:
            gpio.output(index, gpio.LOW)
        else:
            gpio.output(index, gpio.HIGH)
            time.sleep(1)
    else:
        print("Invalid state value. It should 0 or 1")


def setup():
    gpio.setmode(gpio.BCM)
    for pin in led_list:
        gpio.setup(pin, gpio.OUT)

    print_rpi_versions()


def run(index: int, state: int):
    setup()
    power_on_off_led(index, state)
    gpio.cleanup()


if __name__ == '__main__':
    run(LED_1_PIN, 1)
