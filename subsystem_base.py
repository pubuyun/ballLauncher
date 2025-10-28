from abc import ABC, abstractmethod
from time import perf_counter as now
import config
from gpiozero.pins.rpigpio import RPiGPIOFactory
from gpiozero.pins.mock import MockFactory
from gpiozero.pins.pigpio import PiGPIOFactory


class SubsystemBase(ABC):
    def __init__(self):
        self._initialized = False
        self._last_ts = None
        match config.PIN_FACTORY:
            case "RPiGPIOFactory":
                self.pin_factory = RPiGPIOFactory()
            case "MockFactory":
                self.pin_factory = MockFactory()
            case "PiGPIOFactory":
                self.pin_factory = PiGPIOFactory()

    def _dt(self):
        t = now()
        if self._last_ts is None:
            self._last_ts = t
            return 0.0
        dt = t - self._last_ts
        self._last_ts = t
        return dt

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def periodic(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass
