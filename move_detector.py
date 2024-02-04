import init_fake_rpi
import RPi.GPIO as gpio
import time
import os
import platform
import yagmail
from datetime import datetime, timedelta
from picamera import PiCamera
from utils import print_rpi_versions

LED_1_PIN = 17
LED_2_PIN = 27
LED_3_PIN = 22
BUTTON_PIN = 26
PIR_PIN = 4

FREQUENCY = 250
MAX_RANGE = 50

led_list = [LED_1_PIN, LED_2_PIN, LED_3_PIN]

GRADIENT_LED = 1

CAMERA_FOLDER = 'camera'
PATH_SEP = '\\' if platform.system() == "Windows" else '/'

EMAIL = 'pawel.niedziela@gmail.com'


class CameraManager:
    def __init__(self, path_to_folder):
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = (1280, 720)
        CameraManager.__check_or_create_folder(CAMERA_FOLDER)
        self.path_to_folder = path_to_folder + PATH_SEP + CAMERA_FOLDER

    def take_photo(self) -> str:
        day_folder = CameraManager.__generate_new_folder_or_file_name(True)
        CameraManager.__check_or_create_folder(day_folder, CAMERA_FOLDER)

        file_name = CameraManager.__generate_new_folder_or_file_name() + '.jpg'
        full_path = self.path_to_folder + PATH_SEP + day_folder + PATH_SEP + file_name
        self.camera.capture(full_path)
        print(f"Photo taken: {full_path}")
        self.add_log_to_file(day_folder, file_name)
        return full_path

    def add_log_to_file(self, day_folder: str, photo_file_name: str, log_file_name: str = "photo_logs.txt"):
        with open(self.path_to_folder + PATH_SEP + day_folder + PATH_SEP + log_file_name, 'a') as f:
            f.write(photo_file_name)
            f.write('\n')
            f.close()

    @staticmethod
    def __generate_new_folder_or_file_name(only_folder: bool = False) -> str:

        def __add_led_zero(s) -> str:
            return '0' + s if len(s) == 1 else s

        now = datetime.now()
        prefix = "img"
        sep = "_"
        if not only_folder:
            return prefix + sep + sep.join([__add_led_zero(s) for s in
                                            [str(now.year), str(now.month), str(now.day),
                                             str(now.hour), str(now.minute), str(now.second)]])
        else:
            return sep.join([__add_led_zero(s) for s in
                             [str(now.year), str(now.month), str(now.day)]])

    @staticmethod
    def __check_or_create_folder(name: str, root_folder: str = '') -> bool:
        folder_name = root_folder + PATH_SEP + name if len(root_folder) > 0 else name
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
            print(f'Folder created: {folder_name}')
            return True
        return False


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

    def blink_led(self, sleep_time: float, proportion: int):
        signal_high = sleep_time * proportion / MAX_RANGE
        signal_low = sleep_time * (MAX_RANGE - proportion) / MAX_RANGE

        self.power_on()
        time.sleep(signal_high)
        self.power_off()
        time.sleep(signal_low)

    def blink_gradient(self):
        signal_length = 1 / FREQUENCY

        for i in range(1, MAX_RANGE + 1):
            for _ in range(0, 10):
                self.blink_led(sleep_time=signal_length, proportion=i)

        for i in range(MAX_RANGE, 0, -1):
            for _ in range(0, 10):
                self.blink_led(sleep_time=signal_length, proportion=i)


class PIRSensor(RP4Peripheral):
    def __init__(self, gpio_number, io_type):
        super().__init__(gpio_number, io_type)
        self.consecutive_seconds = 3
        self.sleep_time = 0.1

    def detect_movement(self, leds) -> bool:
        if len(leds) < self.consecutive_seconds:
            print("To few LEDs provided")
            return False

        status = gpio.input(self.gpio_number)
        counter = 0
        seconds_counter = -1
        while status == gpio.HIGH and seconds_counter < self.consecutive_seconds:
            time.sleep(self.sleep_time)
            status = gpio.input(self.gpio_number)
            counter += 1
            if counter % (1 / self.sleep_time) == 0:
                seconds_counter += 1
                if seconds_counter in [0, 1, 2]:
                    leds[seconds_counter].power_on()

        for led in leds:
            led.power_off()

        return status == gpio.HIGH


class TactButton(RP4Peripheral):
    def __init__(self, gpio_number, io_type):
        super().__init__(gpio_number, io_type)

    def get_state(self) -> int:
        signal = gpio.input(self.gpio_number)
        if signal == gpio.HIGH:
            return 1
        else:
            return 0


class MovementDetector:
    def __init__(self, with_email: bool = False):
        self.leds = []

        for pin in led_list:
            led = LED(pin, gpio.OUT)
            led.config()
            self.leds.append(led)

        self.pir_sensor = PIRSensor(PIR_PIN, gpio.IN)
        self.pir_sensor.config()

        self.cam_mgr = CameraManager(os.getcwd())

        self.button = TactButton(BUTTON_PIN, gpio.IN)
        self.button.config()

        self.gradient_led = GRADIENT_LED
        self.last_time_photo_taken = datetime.now() - timedelta(minutes=1)

        print("Last time photo taken: " + datetime.strftime(self.last_time_photo_taken, "%H:%M:%S"))

        self.with_email = with_email
        self.email = EMAIL

    def start(self):
        state = self.button.get_state()

        while not state:
            state = self.button.get_state()
            if self.pir_sensor.detect_movement(self.leds):
                print("Movement detected.")
                self.leds[self.gradient_led].blink_gradient()
                current_time = datetime.now()
                diff = current_time - self.last_time_photo_taken
                diff_minutes = diff.days * 24 * 60 + diff.seconds / 60
                if diff_minutes >= 1:
                    file_path = self.cam_mgr.take_photo()
                    self.last_time_photo_taken = datetime.now()
                    self.send_email(attachment=file_path)
                else:
                    print("Last photo taken less then 1 minute ago.")

    def send_email(self, attachment=''):
        if not self.with_email:
            return

        with open(".gmail_password") as f:
            password = f.read()
            f.close()

        dt = datetime.strftime(self.last_time_photo_taken, "%Y.%m.%d, %H:%M:%S")
        yag = yagmail.SMTP(user=self.email, password=password)
        yag.send(to=self.email, subject='Movement detected',
                 contents=f"Movement detected from Raspberry PI at {dt}.",
                 attachments=attachment)


def run():
    gpio.setmode(gpio.BCM)
    print_rpi_versions()

    d = MovementDetector(with_email=True)
    d.start()

    gpio.cleanup()


if __name__ == "__main__":
    run()
