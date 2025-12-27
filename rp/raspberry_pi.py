from gpio_interface import GPIOInterface, GPIOMode, PinConfig, PinMode, PinOutputValue, PullUpDownValue, GpioEventType
from utils import get_gpio, get_logger
import time

FREQUENCY = 250
MAX_RANGE = 50

class RaspBerryPI:
    gpio: GPIOInterface
    pins_config: dict[int, PinConfig]

    def __init__(self, mode: GPIOMode):
        self.logger = get_logger(RaspBerryPI)
        self.gpio = get_gpio()
        self.gpio.setmode(mode)
        self.pins_config = dict()

    def configure_pins(self, pins: list[int], mode: PinMode,
                       initial_value: PinOutputValue = PinOutputValue.LOW,
                       pull_up_down: PullUpDownValue = PullUpDownValue.PULL_DOWN,
                       event_type:GpioEventType = GpioEventType.RISING,
                       callaback=None):
        self.logger.debug(f"Configuring pins: {pins}")
        for pin in pins:
            pin_config = PinConfig(pin_number=pin, mode=mode,
                                   initial_value=initial_value,
                                   event_type=event_type,
                                   pull_up_down=pull_up_down,
                                   callback=callaback)

            if pin in self.pins_config:
                self.logger.warning(f"Warning: Pin {pin} is already configured. Overwriting the configuration.")

            self.pins_config[pin] = pin_config

            if mode == PinMode.OUT:
                self.gpio.setup(pin_number=pin_config.pin_number,
                                mode=pin_config.mode, initial=pin_config.initial_value)
            elif mode == PinMode.IN:
                self.gpio.setup(pin_number=pin_config.pin_number, mode=pin_config.mode,
                                pull_up_down=pin_config.pull_up_down)
                if callaback is not None:
                    self.logger.debug(f"Adding event handler for pin {pin}")
                    self.gpio.add_event_handler(pin_number=pin_config.pin_number,
                                                event_type=pin_config.event_type,
                                                callback=pin_config.callback)
                else:
                    self.logger.warning(f"No callback provided for pin {pin}, skipping event handler setup.")
            else:
                self.logger.error(f"Error: Unsupported Pin mode: {mode}")
                raise ValueError(f"Unsupported Pin mode: {mode}")

    def blink(self, pin: int, blink_count: int = 3, interval: float = 1.0):
        self.logger.debug(f"Blinking pin {pin} for {blink_count} times with interval {interval} seconds.")
        if pin not in self.pins_config:
            self.logger.error(f"Error: Pin {pin} is not configured.")
            return

        for _ in range(blink_count):
            self.gpio.set_output(pin, PinOutputValue.HIGH)
            time.sleep(interval)
            self.gpio.set_output(pin, PinOutputValue.LOW)
            time.sleep(interval)

    def _blink_led(self, pin: int, sleep_time: float, proportion: int):
        signal_high = sleep_time * proportion / MAX_RANGE
        signal_low = sleep_time * (MAX_RANGE - proportion) / MAX_RANGE

        self.gpio.set_output(pin, PinOutputValue.HIGH)
        time.sleep(signal_high)
        self.gpio.set_output(pin, PinOutputValue.LOW)
        time.sleep(signal_low)

    def fade_in_out(self, pin: int, cycles: int = 1):
        self.logger.debug(f"Fading pin {pin} in {cycles} cycles.")
        if pin not in self.pins_config:
            self.logger.error(f"Error: Pin {pin} is not configured.")
            return

        signal_length = 1 / FREQUENCY

        for _ in range(0, cycles):
            for i in range(1, MAX_RANGE + 1):
                for _ in range(0, 10):
                    self._blink_led(pin, signal_length, i)

            for i in range(MAX_RANGE, 0, -1):
                for _ in range(0, 10):
                    self._blink_led(pin, signal_length, i)

    def cleanup(self):
        self.gpio.cleanup()

    def __str__(self):
        return self.gpio.info()
