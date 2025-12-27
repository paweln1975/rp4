from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable


class PinMode(Enum):
    IN = 'IN'
    OUT = 'OUT'


class PinOutputValue(Enum):
    LOW = 0
    HIGH = 1

class GpioEventType(Enum):
    RISING = 'RISING'
    FALLING = 'FALLING'
    BOTH = 'BOTH'


class PullUpDownValue(Enum):
    PULL_UP = 'PULL_UP'
    PULL_DOWN = 'PULL_DOWN'


class PinConfig:
    pin_number: int
    mode: PinMode
    initial_value: PinOutputValue
    event_type: GpioEventType
    pull_up_down: PullUpDownValue
    callback: Callable

    def __init__(self, pin_number: int, mode: PinMode,
                 initial_value: PinOutputValue = PinOutputValue.LOW,
                 event_type: GpioEventType = GpioEventType.RISING,
                 pull_up_down: PullUpDownValue = PullUpDownValue.PULL_DOWN,
                 callback: Callable = None):
        self.pin_number = pin_number
        self.mode = mode
        self.initial_value = initial_value
        self.event_type = event_type
        self.pull_up_down = pull_up_down
        self.callback = callback


class GPIOMode(Enum):
    BCM = 'BCM'
    BOARD = 'BOARD'

class GPIOInterface(ABC):
    @abstractmethod
    def setmode(self, mode: GPIOMode): ...

    @abstractmethod
    def setup(self, pin_number: int, mode: PinMode, initial:PinOutputValue=PinOutputValue.LOW,
              pull_up_down=PullUpDownValue.PULL_DOWN): ...

    @abstractmethod
    def set_output(self, pin_number: int, value: PinOutputValue): ...

    @abstractmethod
    def cleanup(self): ...

    @abstractmethod
    def info(self): ...

    @abstractmethod
    def add_event_handler(self, pin_number: int, event_type: GpioEventType, callback): ...
