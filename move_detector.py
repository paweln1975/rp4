import init_fake_rpi
import RPi.GPIO as gpio
import time
from utils import print_rpi_versions

LED_1_PIN = 17
LED_2_PIN = 27
LED_3_PIN = 22
BUTTON_PIN = 26
PIR_PIN = 4

led_list = [LED_1_PIN, LED_2_PIN, LED_3_PIN]


class CameraManager:
    def __init__(self, path_to_folder):
        self.path_to_folder = path_to_folder


class RP4Peripheral:
    def __init__(self, gpio_number, io_type):
        self.gpio_number = gpio_number
        self.io_type = io_type

    def config(self):
        gpio.setup(self.gpio_number, self.io_type)


class LED(RP4Peripheral):

    def __init__(self, gpio_number, io_type):
        super().__init__(gpio_number, io_type)

    def power_on(self):
        self.power_on_off_led(1)

    def power_off(self):
        self.power_on_off_led(0)

    def power_on_off_led(self, state: int):
        if state not in [0, 1]:
            print(f"Invalid state value. It should be 0 or 1.")
            return

        if state == 0 or state == 1:
            if state == 0:
                gpio.output(self.gpio_number, gpio.LOW)
            else:
                gpio.output(self.gpio_number, gpio.HIGH)

    def config(self):
        super().config()
        self.power_off()


class PIRSensor(RP4Peripheral):
    def __init__(self, gpio_number, io_type):
        super().__init__(gpio_number, io_type)
        self.consecutive_seconds = 3
        self.sleep_time = 0.1

    def detect_movement(self, leds):
        if len(leds) < self.consecutive_seconds:
            print("To few LEDs provided")
            return

        status = gpio.input(self.gpio_number)
        counter = 0
        seconds_counter = -1
        while status == gpio.HIGH and seconds_counter < self.consecutive_seconds - 1:
            time.sleep(self.sleep_time)
            status = gpio.input(self.gpio_number)
            counter += 1
            if counter % (1 / self.sleep_time) == 0:
                seconds_counter += 1
                print(seconds_counter)
                leds[seconds_counter].power_on()


class TactButton(RP4Peripheral):
    def __init__(self, gpio_number, io_type):
        super().__init__(gpio_number, io_type)

    def get_state(self) -> int:
        signal = gpio.input(self.gpio_number)
        if signal == gpio.HIGH:
            return 1
        else:
            return 0


def run():
    gpio.setmode(gpio.BCM)

    leds = []

    for pin in led_list:
        led = LED(pin, gpio.OUT)
        led.config()
        leds.append(led)

    pir = PIRSensor(PIR_PIN, gpio.IN)
    pir.config()

    button = TactButton(BUTTON_PIN, gpio.IN)
    button.config()

    state = button.get_state()

    while not state:
        state = button.get_state()
        pir.detect_movement(leds)

    gpio.cleanup()


if __name__ == "__main__":
    run()
