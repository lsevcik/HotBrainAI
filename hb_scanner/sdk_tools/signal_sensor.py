import contextlib
from abc import abstractmethod, ABC

from __cmn_types import *
from cmn_types import *
from sensor import Sensor


class SignalSensor(Sensor, ABC):
    def __init__(self, ptr):
        super().__init__(ptr)
        if self.is_supported_feature(SensorFeature.FeatureSignal):
            self.signalDataReceived = None
            self.set_signal_callbacks()
        self.__closed = False

    def __del__(self):
        with contextlib.suppress(Exception):
            if not self.__closed:
                self.__closed = True
                self.signalDataReceived = None
                self.unset_signal_callbacks()
        super().__del__()

    @abstractmethod
    def set_signal_callbacks(self):
        pass

    @abstractmethod
    def unset_signal_callbacks(self):
        pass
