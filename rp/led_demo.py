from rp_impl import RaspBerryPI
from gpio_interface import PinMode, PinOutputValue, GPIOMode

LED_PIN = 17

def run():
    rp4 = RaspBerryPI(mode=GPIOMode.BCM)
    rp4.configure_pins(pins=[LED_PIN], mode=PinMode.OUT, initial_value=PinOutputValue.LOW)
    print(rp4)
    rp4.blink(LED_PIN)
    rp4.fade_in_out(LED_PIN)
    rp4.cleanup()

if __name__ == "__main__":
    run()