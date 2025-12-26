from gpio_interface import GPIOInterface, GPIOMode, PinMode, PinOutputValue
from utils import get_logger

class FakeGPIO(GPIOInterface):

    mode: GPIOMode = GPIOMode.BCM
    _state: dict[int, tuple[PinMode, PinOutputValue]] = dict()
    def __init__(self):
        self.logger = get_logger(FakeGPIO)

    def setmode(self, mode: GPIOMode):
        self.logger.info(f"Setting mode to {mode}")
        self.mode = mode

    def setup(self, pin_number: int, mode: PinMode, initial=None):
        self.logger.debug(f"Setup pin {pin_number} as {mode} with initial {initial}")
        self._state[pin_number] = (mode, PinOutputValue.LOW if initial is None else initial)

    def set_output(self, pin_number: int, value: PinOutputValue):
        if pin_number in self._state:
            self._state[pin_number] = (self._state[pin_number][0], value)
            self.logger.debug(f"Setting pin {pin_number} to {value}")
        else:
            self.logger.error(f"Error: Pin {pin_number} is not configured.")

    def cleanup(self):
        self.logger.info(f"Cleaning up pin {self._state}")
        self._state.clear()

    def info(self):
        return "[FAKE GPIO] info()" + \
                f"\nGPIO Mode: {self.mode}" + \
                "\nConfigured pins and their states:" + \
                "\n".join(
                    f"  Pin {pin}: Mode={mode}, Value={value}"
                    for pin, (mode, value) in self._state.items()
                )

