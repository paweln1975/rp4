import init_fake_rpi
import RPi.GPIO as gpio
import time
from utils import print_rpi_versions

LED_1_PIN = 17
LED_2_PIN = 27
LED_3_PIN = 22

led_list = [LED_1_PIN, LED_2_PIN, LED_3_PIN]

print('Running on Real RPi:', init_fake_rpi.IS_REAL_RPI)

def power_on_off_led(index: int, state: int):
    if index not in led_list:
        print(f"Invalid GPIO index value. It should be one of {led_list}")

    if state == 0 or state == 1:
        if state == 0:
            gpio.output(index, gpio.LOW)
        else:
            gpio.output(index, gpio.HIGH)
    else:
        print("Invalid state value. It should 0 or 1")


def setup():
    print_rpi_versions()
    gpio.setmode(gpio.BCM)
    for pin in led_list:
        gpio.setup(pin, gpio.OUT, initial=gpio.LOW)


def run(index: int, blink_count: int = 3):
    setup()
    for _ in range(blink_count):
        power_on_off_led(index, 1)
        time.sleep(1)
        power_on_off_led(index, 0)
        time.sleep(1)
    gpio.cleanup()


if __name__ == '__main__':
    run(LED_1_PIN)
