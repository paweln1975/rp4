from utils import key_pressed, consume_key
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


rp4 = RaspBerryPI(mode=GPIOMode.BCM)

def local_blink(channel: int):
    rp4.logger.debug(f"Button pressed on channel {channel}, blinking LED.")
    for led in LEDS:
        rp4.off(led)
    
    global CURRENT_LED
    CURRENT_LED += 1
    if CURRENT_LED >= len(LEDS):
        CURRENT_LED = 0

    rp4.on(LEDS[CURRENT_LED])

def local_fade(channel: int):
    rp4.logger.debug(f"PIR motion detected on channel {channel}, fading LED.")
    rp4.fade_in_out(LED_RED)

def run():
    rp4.configure_pins(pins=[LED_RED, LED_BLUE, LED_GREEN], mode=PinMode.OUT, initial_value=PinOutputValue.LOW)
    rp4.configure_pins(pins=[BUTTON_PIN], mode=PinMode.IN,
                       pull_up_down=PullUpDownValue.PULL_UP,
                       event_type=GpioEventType.FALLING,
                       callback=local_blink)

    rp4.configure_pins(pins=[PIR_PIN], mode=PinMode.IN,
                        pull_up_down=PullUpDownValue.PULL_UP,
                        event_type=GpioEventType.RISING,
                        callback=local_fade)

    print(rp4)

    rp4.blink(LED_RED, interval=0.5)
    rp4.blink(LED_GREEN, interval=0.5)
    rp4.blink(LED_BLUE, interval=0.5)

    print("Press any key to exit...")

    while True:
        if key_pressed():
            consume_key()
            break
        sleep(0.01)

    rp4.cleanup()

if __name__ == "__main__":
    run()
