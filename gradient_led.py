import init_fake_rpi
import RPi.GPIO as gpio
import time
from utils import print_rpi_versions

LED_PIN = 27
FREQUENCY = 250
MAX_RANGE = 50


def setup():
    gpio.setmode(gpio.BCM)
    gpio.setup(LED_PIN, gpio.OUT)


def blink_led(sleep_time: float, proportion: int):
    signal_high = sleep_time * proportion / MAX_RANGE
    signal_low = sleep_time * (MAX_RANGE - proportion) / MAX_RANGE

    gpio.output(LED_PIN, gpio.HIGH)
    time.sleep(signal_high)
    gpio.output(LED_PIN, gpio.LOW)
    time.sleep(signal_low)


def run():
    setup()
    print_rpi_versions()

    signal_length = 1 / FREQUENCY

    for _ in range(0, 2):
        for i in range(1, MAX_RANGE + 1):
            for _ in range(0, 10):
                blink_led(sleep_time=signal_length, proportion=i)

        for i in range(MAX_RANGE, 0, -1):
            for _ in range(0, 10):
                blink_led(sleep_time=signal_length, proportion=i)

    gpio.cleanup()


if __name__ == "__main__":
    run()
