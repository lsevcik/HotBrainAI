from neurosdk.__utils import raise_exception_if
from neurosdk.__cmn_types import *
from neurosdk.cmn_types import *
from neurosdk.resist_sensor import ResistSensor
from neurosdk.sensor import _neuro_lib
from neurosdk.signal_sensor import SignalSensor


class BrainBitSensor(ResistSensor, SignalSensor):
    def __init__(self, ptr):
        super().__init__(ptr)
        # signatures
        _neuro_lib.addResistCallbackBrainBit.argtypes = [SensorPointer, ResistCallbackBrainBit, c_void_p,
                                                         ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addResistCallbackBrainBit.restype = c_uint8
        _neuro_lib.removeResistCallbackBrainBit.argtypes = [BrainBitResistDataListenerHandle]
        _neuro_lib.removeResistCallbackBrainBit.restype = c_void_p
        _neuro_lib.addSignalDataCallbackBrainBit.argtypes = [SensorPointer, SignalDataCallbackBrainBit, c_void_p,
                                                             ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addSignalDataCallbackBrainBit.restype = c_uint8
        _neuro_lib.removeSignalDataCallbackBrainBit.argtypes = [BrainBitSignalDataListenerHandle]
        _neuro_lib.removeSignalDataCallbackBrainBit.restype = c_void_p

    def __del__(self):
        super().__del__()

    def set_signal_callbacks(self):
        self.__add_signal_data_callback_brain_bit()

    def unset_signal_callbacks(self):
        _neuro_lib.removeSignalDataCallbackBrainBit(self.__signalDataCallbackBrainBitHandle)

    def set_resist_callbacks(self):
        self.__add_resist_callback_brain_bit()

    def unset_resist_callbacks(self):
        _neuro_lib.removeResistCallbackBrainBit(self.__resistCallbackBrainBitHandle)

    def __add_signal_data_callback_brain_bit(self):
        def __py_signal_data_callback_brain_bit(ptr, data, sz_data, user_data):
            signal_data = [BrainBitSignalData(PackNum=int(data[i].PackNum),
                                              Marker=int(data[i].Marker),
                                              O1=float(data[i].O1),
                                              O2=float(data[i].O2),
                                              T3=float(data[i].T3),
                                              T4=float(data[i].T4)) for i in range(sz_data)]
            if user_data.signalDataReceived is not None:
                user_data.signalDataReceived(user_data, signal_data)

        status = OpStatus()
        self.__signalDataCallbackBrainBit = SignalDataCallbackBrainBit(__py_signal_data_callback_brain_bit)
        self.__signalDataCallbackBrainBitHandle = BrainBitSignalDataListenerHandle()
        _neuro_lib.addSignalDataCallbackBrainBit(self.sensor_ptr, self.__signalDataCallbackBrainBit,
                                                 byref(self.__signalDataCallbackBrainBitHandle),
                                                 py_object(self), byref(status))
        raise_exception_if(status)

    def __add_resist_callback_brain_bit(self):
        def __py_resist_callback_brain_bit(ptr, data, user_data):
            resist = BrainBitResistData(O1=float(data.O1),
                                        O2=float(data.O2),
                                        T3=float(data.T3),
                                        T4=float(data.T4))
            if user_data.resistDataReceived is not None:
                user_data.resistDataReceived(user_data, resist)

        status = OpStatus()
        self.__resistCallbackBrainBit = ResistCallbackBrainBit(__py_resist_callback_brain_bit)
        self.__resistCallbackBrainBitHandle = BrainBitResistDataListenerHandle()
        _neuro_lib.addResistCallbackBrainBit(self.sensor_ptr, self.__resistCallbackBrainBit,
                                             byref(self.__resistCallbackBrainBitHandle),
                                             py_object(self), byref(status))
        raise_exception_if(status)
