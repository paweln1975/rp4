from utils import key_pressed, consume_key
from time import sleep
from raspberry_pi import RaspBerryPI
from gpio_interface import PinMode, PinOutputValue, GPIOMode, PullUpDownValue, GpioEventType

LED_RED = 17
LED_GREEN = 22
LED_BLUE = 27

LEDS = [LED_RED, LED_BLUE, LED_GREEN]

CURRENT_LED = -1

BUTTON_PIN = 26

rp4 = RaspBerryPI(mode=GPIOMode.BCM)

def local_blink(channel: int):
    rp4.logger.debug(f"Button pressed on channel {channel}, blinking LED.")
    rp4.off(LED_RED)
    rp4.off(LED_GREEN)
    rp4.off(LED_BLUE)
    
    global CURRENT_LED
    CURRENT_LED += 1
    if CURRENT_LED >= len(LEDS):
        CURRENT_LED = 0

    rp4.on(LEDS[CURRENT_LED])

def run():
    rp4.configure_pins(pins=[LED_RED, LED_BLUE, LED_GREEN], mode=PinMode.OUT, initial_value=PinOutputValue.LOW)
    rp4.configure_pins(pins=[BUTTON_PIN], mode=PinMode.IN,
                       pull_up_down=PullUpDownValue.PULL_UP,
                       event_type=GpioEventType.FALLING,
                       callaback=local_blink)

    print(rp4)

    rp4.blink(LED_RED, interval=0.5)
    rp4.blink(LED_GREEN, interval=0.5)
    rp4.blink(LED_BLUE, interval=0.5)
    # rp4.fade_in_out(LED_PIN)

    local_blink(BUTTON_PIN)
    print("Press any key to exit...")

    while True:
        if key_pressed():
            consume_key()
            break
        sleep(0.01)

    rp4.cleanup()

if __name__ == "__main__":
    run()
