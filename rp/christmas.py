from time import sleep
from raspberry_pi import RaspBerryPI
from gpio_interface import PinMode, PinOutputValue, GPIOMode, PullUpDownValue, GpioEventType

PIN_LIGHTS = 21
BUTTON_PIN = 26
PIR_PIN = 4

SYSTEM_ENABLED = True
MOVEMENT_DETECTED = False

BLINK_COUNT = 5
ON_OFF_TIME = 0.5

rp4 = RaspBerryPI(mode=GPIOMode.BCM)


def system_enabled_handler(channel: int):
    global SYSTEM_ENABLED
    SYSTEM_ENABLED = not SYSTEM_ENABLED
    if SYSTEM_ENABLED:
        rp4.logger.info(f"Button pressed on channel {channel}, system enabled.")
    else:
        rp4.logger.info(f"Button pressed on channel {channel}, system disabled.")


def movement_detector_handler(channel: int):
    global MOVEMENT_DETECTED
    if not SYSTEM_ENABLED:
        return
    rp4.logger.debug(f"PIR motion detected on channel {channel}, blinking lights.")
    MOVEMENT_DETECTED = True

def run():
    rp4.configure_pins(pins=[PIN_LIGHTS], mode=PinMode.OUT, initial_value=PinOutputValue.LOW)
    rp4.configure_pins(pins=[BUTTON_PIN], mode=PinMode.IN,
                       pull_up_down=PullUpDownValue.PULL_UP,
                       event_type=GpioEventType.FALLING,
                       callback=system_enabled_handler)

    rp4.configure_pins(pins=[PIR_PIN], mode=PinMode.IN,
                       pull_up_down=PullUpDownValue.PULL_UP,
                       event_type=GpioEventType.RISING,
                       callback=movement_detector_handler)

    print(rp4)
    while SYSTEM_ENABLED:
        sleep(0.01)
        rp4.fade_in_out(PIN_LIGHTS)

        global MOVEMENT_DETECTED
        if MOVEMENT_DETECTED:
            for _ in range(BLINK_COUNT):
                rp4.on(PIN_LIGHTS)
                sleep(ON_OFF_TIME)
                rp4.off(PIN_LIGHTS)
                sleep(ON_OFF_TIME)
            MOVEMENT_DETECTED = False

    rp4.cleanup()


if __name__ == "__main__":
    run()
