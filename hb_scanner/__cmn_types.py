from ctypes import *
import ctypes

ERR_MSG_LEN = 512
SENSOR_NAME_LEN = 256
SENSOR_ADR_LEN = 128
SENSOR_SN_LEN = 128
SENSOR_CHANNEL_NAME_LEN = 8

SensorScannerPointer = POINTER(c_void_p)
SensorPointer = POINTER(c_void_p)

SizeType = POINTER(c_int32)
EnumType = POINTER(c_int8)


class OpStatus(Structure):
    _fields_ = [
        ('Success', c_ubyte),
        ('Error', c_uint),
        ('ErrorMsg', c_char * ERR_MSG_LEN)
    ]


class NativeSensorVersion(Structure):
    _fields_ = [
        ('FwMajor', c_uint32),
        ('FwMinor', c_uint32),
        ('FwPatch', c_uint32),

        ('HwMajor', c_uint32),
        ('HwMinor', c_uint32),
        ('HwPatch', c_uint32),

        ('ExtMajor', c_uint32)
    ]


class NativeSensorInfo(Structure):
    _fields_ = [
        ('SensFamily', c_uint8),
        ('SensModel', c_uint8),
        ('Name', c_char * SENSOR_NAME_LEN),
        ('Address', c_char * SENSOR_ADR_LEN),
        ('SerialNumber', c_char * SENSOR_SN_LEN),
        ('PairingRequired', c_uint8),
    ]


class NativeParameterInfo(Structure):
    _fields_ = [
        ('Param', c_uint8),
        ('ParamAccess', c_uint8),
    ]


SensorCallbackScanner = CFUNCTYPE(c_void_p, SensorScannerPointer, POINTER(NativeSensorInfo), c_int32, ctypes.py_object)
SensorsListenerHandle = POINTER(c_void_p)

BatteryCallback = CFUNCTYPE(c_void_p, SensorPointer, c_int32, ctypes.py_object)
BattPowerListenerHandle = POINTER(c_void_p)

ConnectionStateCallback = CFUNCTYPE(c_void_p, SensorPointer, c_int8, ctypes.py_object)
SensorStateListenerHandle = POINTER(c_void_p)


class NativeCallibriStimulatorMAState(Structure):
    _fields_ = [
        ('StimulatorState', c_uint8),
        ('MAState', c_uint8)
    ]


# Stimulator parameters
# Limitations:
# (Current * Frequency * PulseWidth / 100) <= 2300 uA
class NativeCallibriStimulationParams(Structure):
    _fields_ = [
        # Stimulus amplitude in  mA. 1..100
        ('Current', c_uint8),
        # Duration of the stimulating pulse by us. 20..460
        ('PulseWidth', c_uint16),
        # Frequency of stimulation impulses by Hz. 1..200.
        ('Frequency', c_uint8),
        # Maximum stimulation time by ms. 0...65535.
        ('StimulusDuration', c_uint16)
    ]


class NativeCallibriMotionAssistantParams(Structure):
    _fields_ = [
        ('GyroStart', c_uint8),
        ('GyroStop', c_uint8),
        ('Limb', c_uint8),
        # multiple of 10. This means that the device is using the (MinPauseMs / 10) value.;</br>
        # Correct values: 10, 20, 30, 40 ...
        ('MinPauseMs', c_uint8)
    ]


class NativeCallibriMotionCounterParam(Structure):
    _fields_ = [
        # Insense threshold mg. 0..500
        ('InsenseThresholdMG', c_uint16),
        # Algorithm insense threshold in time (in samples with the MEMS sampling rate) 0..500
        ('InsenseThresholdSample', c_uint16),
    ]


class NativeCallibriSignalData(Structure):
    _fields_ = [
        ('PackNum', c_uint32),
        ('Samples', POINTER(c_double)),
        ('SzSamples', c_uint32)
    ]


class NativeCallibriRespirationData(Structure):
    _fields_ = [
        ('PackNum', c_uint32),
        ('Samples', POINTER(c_double)),
        ('SzSamples', c_uint32)
    ]


class NativeQuaternionData(Structure):
    _fields_ = [
        ('PackNum', c_uint32),
        ('W', c_double),
        ('X', c_double),
        ('Y', c_double),
        ('Z', c_double)
    ]


class NativeCallibriEnvelopeData(Structure):
    _fields_ = [
        ('PackNum', c_uint32),
        ('Sample', c_double)
    ]


SignalCallbackCallibri = CFUNCTYPE(c_void_p, SensorPointer, POINTER(NativeCallibriSignalData), c_int32,
                                   ctypes.py_object)
CallibriSignalDataListenerHandle = POINTER(c_void_p)

RespirationCallbackCallibri = CFUNCTYPE(c_void_p, SensorPointer, POINTER(NativeCallibriRespirationData), c_int32,
                                        ctypes.py_object)
CallibriRespirationDataListenerHandle = POINTER(c_void_p)

ElectrodeStateCallbackCallibri = CFUNCTYPE(c_void_p, SensorPointer, c_uint8, ctypes.py_object)
CallibriElectrodeStateListenerHandle = POINTER(c_void_p)

QuaternionDataCallback = CFUNCTYPE(c_void_p, SensorPointer, POINTER(NativeQuaternionData), c_int32, ctypes.py_object)
QuaternionDataListenerHandle = POINTER(c_void_p)

EnvelopeDataCallbackCallibri = CFUNCTYPE(c_void_p, SensorPointer, POINTER(NativeCallibriEnvelopeData), c_int32,
                                         ctypes.py_object)
CallibriEnvelopeDataListenerHandle = POINTER(c_void_p)


class NativePoint3D(Structure):
    _fields_ = [
        ('X', c_double),
        ('Y', c_double),
        ('Z', c_double)
    ]


class NativeMEMSData(Structure):
    _fields_ = [
        ('PackNum', c_uint32),
        ('Accelerometer', NativePoint3D),
        ('Gyroscope', NativePoint3D)
    ]

    
MEMSDataCallback = CFUNCTYPE(c_void_p, SensorPointer, POINTER(NativeMEMSData), c_int32, ctypes.py_object)
MEMSDataListenerHandle = POINTER(c_void_p)


class NativeBrainBitSignalData(Structure):
    _fields_ = [
        ('PackNum', c_uint32),
        ('Marker', c_uint8),
        ('O1', c_double),
        ('O2', c_double),
        ('T3', c_double),
        ('T4', c_double),
    ]


class NativeBrainBitResistData(Structure):
    _fields_ = [
        ('O1', c_double),
        ('O2', c_double),
        ('T3', c_double),
        ('T4', c_double),
    ]


ResistCallbackBrainBit = CFUNCTYPE(c_void_p, SensorPointer, NativeBrainBitResistData, ctypes.py_object)
BrainBitResistDataListenerHandle = POINTER(c_void_p)

SignalDataCallbackBrainBit = CFUNCTYPE(c_void_p, SensorPointer, POINTER(NativeBrainBitSignalData), c_int32,
                                       ctypes.py_object)
BrainBitSignalDataListenerHandle = POINTER(c_void_p)


class NativeFPGData(Structure):
    _fields_ = [
        ('PackNum', c_uint32),
        ('IrAmplitude', c_double),
        ('RedAmplitude', c_double),
    ]


FPGDataCallbackNeuroSmart = CFUNCTYPE(c_void_p, SensorPointer, POINTER(NativeFPGData), c_int32, ctypes.py_object)
FPGDataListenerHandle = POINTER(c_void_p)


AmpModeCallback = CFUNCTYPE(c_void_p, SensorPointer, c_uint8, ctypes.py_object)
AmpModeListenerHandle = POINTER(c_void_p)
