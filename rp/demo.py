from datetime import datetime
from time import sleep
from raspberry_pi import RaspBerryPI
from gpio_interface import PinMode, PinOutputValue, GPIOMode, PullUpDownValue, GpioEventType
from generate_gallery import build_gallery_for_day

LED_RED = 17
LED_GREEN = 22
LED_BLUE = 27

LEDS = [LED_RED, LED_GREEN, LED_BLUE]

CURRENT_LED = -1
BUTTON_PIN = 26
PIR_PIN = 4

SYSTEM_ENABLED = True
MOVEMENT_DETECTED = False

PHOTO_TIME_DELTA_IN_SEC = 60.0 * 5

HOUR_START = 6
HOUR_END = 20

def system_enabled_handler(channel: int):
    global SYSTEM_ENABLED
    SYSTEM_ENABLED = not SYSTEM_ENABLED

def movement_detector_handler(channel: int):
    global MOVEMENT_DETECTED
    if not SYSTEM_ENABLED:
        return
    MOVEMENT_DETECTED = True

def enable_led(rp: RaspBerryPI, led_pin: int, break_time: float = 2.0, light_time: float = 0.1):
    rp.on(led_pin)
    sleep(light_time)
    for led in LEDS:
        rp.off(led)
    sleep(break_time)

def enable_leds(rp: RaspBerryPI, sleep_time: float = 0.5):
    for led in LEDS:
        rp.off(led)

    sleep(sleep_time)
    global CURRENT_LED
    CURRENT_LED += 1
    if CURRENT_LED >= len(LEDS):
        CURRENT_LED = 0

    rp.on(LEDS[CURRENT_LED])
    sleep(sleep_time)

def config() -> RaspBerryPI:
    rp4 = RaspBerryPI(mode=GPIOMode.BCM)
    # rp4.configure_pins(pins=[LED_RED, LED_BLUE, LED_GREEN], mode=PinMode.OUT, initial_value=PinOutputValue.LOW)
    # rp4.configure_pins(pins=[BUTTON_PIN], mode=PinMode.IN,
    #                    pull_up_down=PullUpDownValue.PULL_UP,
    #                    event_type=GpioEventType.FALLING,
    #                    callback=system_enabled_handler)
    #
    # rp4.configure_pins(pins=[PIR_PIN], mode=PinMode.IN,
    #                     pull_up_down=PullUpDownValue.PULL_UP,
    #                     event_type=GpioEventType.RISING,
    #                     callback=movement_detector_handler)

    rp4.add_led(LED_RED) \
        .add_led(LED_GREEN) \
        .add_led(LED_BLUE) \
        .add_button(BUTTON_PIN, system_enabled_handler) \
        # .add_move_detector(PIR_PIN, movement_detector_handler)

    rp4.logger.info("Raspberry Pi configured successfully for LED demo.")
    print(rp4)
    return rp4

def take_photo(rp: RaspBerryPI, last_photo_time: datetime) -> datetime:
    current_time = datetime.now()

    # generate photo only when hour is between start and end
    if HOUR_START <= current_time.hour <= HOUR_END:
        if (current_time - last_photo_time).total_seconds() > PHOTO_TIME_DELTA_IN_SEC:
            last_photo_time = current_time
            rp.logger.info(f"Taking photo")
            # Red led fade out to starting the photo
            rp.fade_in_out(LED_RED)
            rp.take_photo()
            build_gallery_for_day(root_path="/home/pi/Pictures", output_dir="/home/pi/Pictures")
    return last_photo_time

def run(rp: RaspBerryPI = None):
    if rp is None:
        rp = config()

    # Initial LED sequence to indicate the system is ready
    for _ in range(3):
        enable_leds(rp)

    last_photo_time = datetime(2026, 1, 1)

    while SYSTEM_ENABLED:
        # Green led blink to indicate system is working
        enable_led(rp, LED_GREEN)
        sleep(0.01)
        # global MOVEMENT_DETECTED
        # if MOVEMENT_DETECTED:
        #     current_led = LEDS[CURRENT_LED]
        #     rp.logger.info(f"Movement detected! Fading LED for PIN={current_led}")
        #     rp.fade_in_out(current_led)
        #     rp.take_photo()
        #     MOVEMENT_DETECTED = False
        last_photo_time = take_photo(rp, last_photo_time)


    rp.cleanup()

if __name__ == "__main__":
    run()
