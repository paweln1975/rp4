import RPi.GPIO as gpio
from collections.abc import Callable
from gpio_interface import GPIOInterface, GPIOMode, PinMode, PinOutputValue, GpioEventType, PullUpDownValue
from importlib.metadata import version

class RealGPIO(GPIOInterface):

    def setmode(self, mode: GPIOMode):
        if mode == GPIOMode.BCM:
            gpio.setmode(gpio.BCM)
        elif mode == GPIOMode.BOARD:
            gpio.setmode(gpio.BOARD)
        else:
            raise ValueError(f"Unsupported GPIO mode: {mode}")

    def setup(self, pin_number: int, mode: PinMode,
              initial=PinOutputValue.LOW,
              pull_up_down=PullUpDownValue.PULL_DOWN):

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

        if pull_up_down == PullUpDownValue.PULL_UP:
            pud = gpio.PUD_UP
        elif pull_up_down == PullUpDownValue.PULL_DOWN:
            pud = gpio.PUD_DOWN
        else:
            raise ValueError(f"Unsupported pull up/down value: {pull_up_down}")

        if mode == gpio.OUT:
            gpio.setup(pin_number, mode, initial=initial)
        else:
            gpio.setup(pin_number, mode, pull_up_down=pud)


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

    def add_event_handler(self, pin_number: int, event_type: GpioEventType, callback: Callable):
        if event_type == GpioEventType.RISING:
            gpio_event = gpio.RISING
        elif event_type == GpioEventType.FALLING:
            gpio_event = gpio.FALLING
        elif event_type == GpioEventType.BOTH:
            gpio_event = gpio.BOTH
        else:
            raise ValueError(f"Unsupported event type: {event_type}")

        gpio.add_event_detect(pin_number, gpio_event, callback=callback)

