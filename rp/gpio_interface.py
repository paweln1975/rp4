from abc import ABC, abstractmethod
from enum import Enum

class PinMode(Enum):
    IN = 'IN'
    OUT = 'OUT'


class PinOutputValue(Enum):
    LOW = 0
    HIGH = 1


class PinConfig:
    pin_number: int
    mode: PinMode
    initial_value: PinOutputValue

    def __init__(self, pin_number: int, mode: PinMode, initial_value: PinOutputValue):
        self.pin_number = pin_number
        self.mode = mode
        self.initial_value = initial_value


class GPIOMode(Enum):
    BCM = 'BCM'
    BOARD = 'BOARD'

class GPIOInterface(ABC):
    @abstractmethod
    def setmode(self, mode: GPIOMode): ...

    @abstractmethod
    def setup(self, pin_number: int, mode: PinMode, initial=PinOutputValue.LOW): ...

    @abstractmethod
    def set_output(self, pin_number: int, value: PinOutputValue): ...

    @abstractmethod
    def cleanup(self): ...

    @abstractmethod
    def info(self): ...
