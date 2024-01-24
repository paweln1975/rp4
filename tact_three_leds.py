import init_fake_rpi
import RPi.GPIO as gpio
import time
from utils import print_rpi_versions

LED_1_PIN = 17
LED_2_PIN = 27
LED_3_PIN = 22
BUTTON_PIN = 26
MAX_TICS = 50

led_list = [LED_1_PIN, LED_2_PIN, LED_3_PIN]


def power_on_led(index: int):
    for led_num in led_list:
        if led_num == index:
            gpio.output(led_num, gpio.HIGH)
        else:
            gpio.output(led_num, gpio.LOW)


def setup():
    print(f"Press the button a few times")
    gpio.setmode(gpio.BCM)
    gpio.setup(LED_1_PIN, gpio.OUT)
    gpio.setup(LED_2_PIN, gpio.OUT)
    gpio.setup(LED_3_PIN, gpio.OUT)
    gpio.setup(BUTTON_PIN, gpio.IN)
    power_on_led(-1)


print_rpi_versions()
setup()

prev_value = gpio.LOW
led_index = 0
led_index_max = len(led_list) - 1
counter = 0

while counter < MAX_TICS:
    value = gpio.input(BUTTON_PIN)
    if value == gpio.HIGH:
        counter += 1
    if value != prev_value:
        prev_value = value
        if value == gpio.LOW:
            power_on_led(led_list[led_index])
            led_index += 1
            if led_index > led_index_max:
                led_index = 0
    time.sleep(0.1)

gpio.cleanup()