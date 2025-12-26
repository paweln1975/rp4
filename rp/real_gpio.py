from gpio_interface import GPIOInterface, GPIOMode, PinMode, PinOutputValue
import RPi.GPIO as gpio
from importlib.metadata import version

class RealGPIO(GPIOInterface):

    def setmode(self, mode: GPIOMode):
        if mode == GPIOMode.BCM:
            gpio.setmode(gpio.BCM)
        elif mode == GPIOMode.BOARD:
            gpio.setmode(gpio.BOARD)
        else:
            raise ValueError(f"Unsupported GPIO mode: {mode}")

    def setup(self, pin_number: int, mode: PinMode, initial=PinOutputValue.LOW):
        if mode == PinMode.IN:
            mode = gpio.IN
        elif mode == PinMode.OUT:
            mode = gpio.OUT
        else:
            raise ValueError(f"Unsupported Pin mode: {mode}")

        if initial == PinOutputValue.LOW or initial is None:
            initial = gpio.LOW
        elif initial == PinOutputValue.HIGH:
            initial = gpio.HIGH
        else:
            raise ValueError(f"Unsupported initial value: {initial}")

        if mode == gpio.OUT:
            gpio.setup(pin_number, mode, initial=initial)
        else:
            gpio.setup(pin_number, mode)


    def set_output(self, pin_number: int, value: PinOutputValue):
        if value == PinOutputValue.LOW:
            gpio.output(pin_number, gpio.LOW)
        elif value == PinOutputValue.HIGH:
            gpio.output(pin_number, gpio.HIGH)
        else:
            raise ValueError(f"Unsupported output value: {value}")

    def cleanup(self):
        gpio.cleanup()

    def info(self):
        info = gpio.RPI_INFO
        return "[REAL GPIO] RPi Info:" + \
               f"\n  REVISION: {info['REVISION']}" + \
               f"\n  TYPE: {info['TYPE']}" + \
               f"\n  MANUFACTURER: {info['MANUFACTURER']}" + \
               f"\n  PROCESSOR version: {info['PROCESSOR']}" + \
               f"\n  RAM: {info['RAM']}" + \
               f"\n  RPi.GPIO version: {version('RPi.GPIO')}"
