import contextlib
from abc import abstractmethod, ABC

from __utils import raise_exception_if
from __cmn_types import *
from cmn_types import *
from sensor import Sensor, _neuro_lib


class ResistSensor(Sensor, ABC):
    def __init__(self, ptr):
        super().__init__(ptr)
        # signatures
        if super().is_supported_parameter(SensorParameter.ParameterSamplingFrequencyResist):
            _neuro_lib.readSamplingFrequencyResistSensor.argtypes = [SensorPointer, POINTER(c_int8), POINTER(OpStatus)]
            _neuro_lib.readSamplingFrequencyResistSensor.restype = c_uint8
        if self.is_supported_feature(SensorFeature.FeatureResist):
            self.resistDataReceived = None
            self.set_resist_callbacks()
        self.__closed = False

    def __del__(self):
        with contextlib.suppress(Exception):
            if not self.__closed:
                self.__closed = True
                self.resistDataReceived = None
                self.unset_resist_callbacks()
        super().__del__()

    @property
    def sampling_frequency_resist(self) -> SensorSamplingFrequency:
        if super().is_supported_parameter(SensorParameter.ParameterSamplingFrequencyResist):
            status = OpStatus()
            sampling_frequency_out = EnumType(c_int8(1))
            _neuro_lib.readSamplingFrequencyResistSensor(self.sensor_ptr, sampling_frequency_out)
            raise_exception_if(status)
            return SensorSamplingFrequency(sampling_frequency_out.contents.value)
        return SensorSamplingFrequency.FrequencyUnsupported

    @abstractmethod
    def set_resist_callbacks(self):
        pass

    @abstractmethod
    def unset_resist_callbacks(self):
        pass
