from time import sleep
from raspberry_pi import RaspBerryPI
from gpio_interface import PinMode, PinOutputValue, GPIOMode, PullUpDownValue, GpioEventType

LED_RED = 17
LED_GREEN = 22
LED_BLUE = 27

LEDS = [LED_RED, LED_GREEN, LED_BLUE]

CURRENT_LED = -1
BUTTON_PIN = 26
PIR_PIN = 4

SYSTEM_ENABLED = True
MOVEMENT_DETECTED = False

def system_enabled_handler(channel: int):
    global SYSTEM_ENABLED
    SYSTEM_ENABLED = not SYSTEM_ENABLED

def movement_detector_handler(channel: int):
    global MOVEMENT_DETECTED
    if not SYSTEM_ENABLED:
        return
    MOVEMENT_DETECTED = True


def enable_led(rp: RaspBerryPI, sleep_time: float = 0.5):
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
    rp4.configure_pins(pins=[LED_RED, LED_BLUE, LED_GREEN], mode=PinMode.OUT, initial_value=PinOutputValue.LOW)
    rp4.configure_pins(pins=[BUTTON_PIN], mode=PinMode.IN,
                       pull_up_down=PullUpDownValue.PULL_UP,
                       event_type=GpioEventType.FALLING,
                       callback=system_enabled_handler)

    rp4.configure_pins(pins=[PIR_PIN], mode=PinMode.IN,
                        pull_up_down=PullUpDownValue.PULL_UP,
                        event_type=GpioEventType.RISING,
                        callback=movement_detector_handler)

    rp4.logger.info("Raspberry Pi configured successfully for LED demo.")
    print(rp4)

    return rp4

def run(rp: RaspBerryPI = None):
    if rp is None:
        rp = config()

    while SYSTEM_ENABLED:
        enable_led(rp)
        sleep(0.01)
        global MOVEMENT_DETECTED
        if MOVEMENT_DETECTED:
            current_led = LEDS[CURRENT_LED]
            rp.logger.info(f"Movement detected! Fading LED for PIN={current_led}")
            rp.fade_in_out(current_led)
            MOVEMENT_DETECTED = False

    rp.cleanup()

if __name__ == "__main__":
    run()
