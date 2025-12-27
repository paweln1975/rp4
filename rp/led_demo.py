from raspberry_pi import RaspBerryPI
from gpio_interface import PinMode, PinOutputValue, GPIOMode, PullUpDownValue, GpioEventType

LED_PIN = 17
BUTTON_PIN = 26

def run():
    rp4 = RaspBerryPI(mode=GPIOMode.BCM)
    rp4.configure_pins(pins=[LED_PIN], mode=PinMode.OUT, initial_value=PinOutputValue.LOW)
    rp4.configure_pins(pins=[BUTTON_PIN], mode=PinMode.IN,
                       pull_up_down=PullUpDownValue.PULL_DOWN,
                       event_type=GpioEventType.RISING,
                       callaback=lambda channel: print(f"Button on pin {channel} pressed!"))

    print(rp4)
    rp4.blink(LED_PIN)
    rp4.fade_in_out(LED_PIN)
    rp4.cleanup()

if __name__ == "__main__":
    run()