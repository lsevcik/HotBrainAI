import contextlib

from neurosdk.__utils import raise_exception_if
from neurosdk.__cmn_types import *
from neurosdk.cmn_types import *

import platform
import pathlib
import sys

_libname = None
if sys.platform == "win32":
    arc = platform.architecture()
    if arc[0].__contains__("64"):
        _libname = pathlib.Path(__file__).parent.resolve() / "libs" / "neurosdk2-x64.dll"
    else:
        _libname = pathlib.Path(__file__).parent.resolve() / "libs" / "neurosdk2-x32.dll"
elif sys.platform.startswith("linux"):
    print('Add linux lib')
elif sys.platform == "darwin":
    print('Add macos lib')
else:
    raise Exception("This platform (%s) is currently not supported by py_neurosdk." % sys.platform)

_neuro_lib = CDLL(str(_libname))


class Sensor:
    def __init__(self, ptr):
        """
        Don't use it to creation device

        -----------
        :param ptr:
            Inner pointer to Sensor object
        """
        # signatures
        _neuro_lib.freeSensor.argtypes = [SensorPointer]
        _neuro_lib.freeSensor.restype = c_void_p
        _neuro_lib.connectSensor.argtypes = [SensorPointer, POINTER(OpStatus)]
        _neuro_lib.connectSensor.restype = c_uint8
        _neuro_lib.disconnectSensor.argtypes = [SensorPointer, POINTER(OpStatus)]
        _neuro_lib.disconnectSensor.restype = c_uint8
        _neuro_lib.getFeaturesCountSensor.argtypes = [SensorPointer]
        _neuro_lib.getFeaturesCountSensor.restype = c_int32
        _neuro_lib.getFeaturesSensor.argtypes = [SensorPointer, POINTER(c_int8), POINTER(c_int32), POINTER(OpStatus)]
        _neuro_lib.getFeaturesSensor.restype = c_uint8
        _neuro_lib.isSupportedFeatureSensor.argtypes = [SensorPointer, c_int8]
        _neuro_lib.isSupportedFeatureSensor.restype = c_int8
        _neuro_lib.getCommandsCountSensor.argtypes = [SensorPointer]
        _neuro_lib.getCommandsCountSensor.restype = c_int32
        _neuro_lib.getCommandsSensor.argtypes = [SensorPointer, POINTER(c_int8), POINTER(c_int32), POINTER(OpStatus)]
        _neuro_lib.getCommandsSensor.restype = c_uint8
        _neuro_lib.isSupportedCommandSensor.argtypes = [SensorPointer, c_int8]
        _neuro_lib.isSupportedCommandSensor.restype = c_int8
        _neuro_lib.getParametersCountSensor.argtypes = [SensorPointer]
        _neuro_lib.getParametersCountSensor.restype = c_int32
        _neuro_lib.getParametersSensor.argtypes = [SensorPointer, POINTER(NativeParameterInfo), POINTER(c_int32), 
                                                   POINTER(OpStatus)]
        _neuro_lib.getParametersSensor.restype = c_uint8
        _neuro_lib.isSupportedParameterSensor.argtypes = [SensorPointer, c_int8]
        _neuro_lib.isSupportedParameterSensor.restype = c_int8
        _neuro_lib.getChannelsCountSensor.argtypes = [SensorPointer]
        _neuro_lib.getChannelsCountSensor.restype = c_int32
        _neuro_lib.execCommandSensor.argtypes = [SensorPointer, c_int8, POINTER(OpStatus)]
        _neuro_lib.execCommandSensor.restype = c_uint8
        _neuro_lib.getFamilySensor.argtypes = [SensorPointer]
        _neuro_lib.getFamilySensor.restype = c_int8
        _neuro_lib.readNameSensor.argtypes = [SensorPointer, c_char_p, c_int32, POINTER(OpStatus)]
        _neuro_lib.readNameSensor.restype = c_uint8
        _neuro_lib.writeNameSensor.argtypes = [SensorPointer, c_char_p, c_int32, POINTER(OpStatus)]
        _neuro_lib.writeNameSensor.restype = c_uint8
        _neuro_lib.readStateSensor.argtypes = [SensorPointer, POINTER(c_int8), POINTER(OpStatus)]
        _neuro_lib.readStateSensor.restype = c_uint8
        _neuro_lib.readAddressSensor.argtypes = [SensorPointer, c_char_p, c_int32, POINTER(OpStatus)]
        _neuro_lib.readAddressSensor.restype = c_uint8
        _neuro_lib.readSerialNumberSensor.argtypes = [SensorPointer, c_char_p, c_int32, POINTER(OpStatus)]
        _neuro_lib.readSerialNumberSensor.restype = c_uint8
        _neuro_lib.writeSerialNumberSensor.argtypes = [SensorPointer, c_char_p, c_int32, POINTER(OpStatus)]
        _neuro_lib.writeSerialNumberSensor.restype = c_uint8
        _neuro_lib.readBattPowerSensor.argtypes = [SensorPointer, POINTER(c_int32), POINTER(OpStatus)]
        _neuro_lib.readBattPowerSensor.restype = c_uint8
        _neuro_lib.readSamplingFrequencySensor.argtypes = [SensorPointer, POINTER(c_int8), POINTER(OpStatus)]
        _neuro_lib.readSamplingFrequencySensor.restype = c_uint8
        _neuro_lib.readGainSensor.argtypes = [SensorPointer, POINTER(c_int8), POINTER(OpStatus)]
        _neuro_lib.readGainSensor.restype = c_uint8
        _neuro_lib.readDataOffsetSensor.argtypes = [SensorPointer, POINTER(c_uint8), POINTER(OpStatus)]
        _neuro_lib.readDataOffsetSensor.restype = c_uint8
        _neuro_lib.readFirmwareModeSensor.argtypes = [SensorPointer, POINTER(c_int8), POINTER(OpStatus)]
        _neuro_lib.readFirmwareModeSensor.restype = c_uint8
        _neuro_lib.readVersionSensor.argtypes = [SensorPointer, POINTER(NativeSensorVersion), POINTER(OpStatus)]
        _neuro_lib.readVersionSensor.restype = c_uint8
        _neuro_lib.addBatteryCallback.argtypes = [SensorPointer, BatteryCallback, c_void_p, ctypes.py_object, 
                                                  POINTER(OpStatus)]
        _neuro_lib.addBatteryCallback.restype = c_uint8
        _neuro_lib.removeBatteryCallback.argtypes = [BattPowerListenerHandle]
        _neuro_lib.removeBatteryCallback.restype = c_void_p
        _neuro_lib.addConnectionStateCallback.argtypes = [SensorPointer, ConnectionStateCallback, c_void_p,
                                                          ctypes.py_object, POINTER(OpStatus)]
        _neuro_lib.addConnectionStateCallback.restype = c_uint8
        _neuro_lib.removeConnectionStateCallback.argtypes = [SensorStateListenerHandle]
        _neuro_lib.removeConnectionStateCallback.restype = c_void_p

        self.sensor_ptr = ptr

        self.sensorStateChanged = None
        self.__add_connection_state_callback()

        if self.is_supported_parameter(SensorParameter.ParameterBattPower):
            self.batteryChanged = None
            self.__add_battery_callback()

        self.__closed = False

    def __del__(self):
        with contextlib.suppress(Exception):
            if not self.__closed:
                self.__closed = True

                self.batteryChanged = None
                self.sensorStateChanged = None

                _neuro_lib.removeBatteryCallback(self.__batteryCallbackHandle)
                _neuro_lib.removeConnectionStateCallback(self.__connectionStateCallbackHandle)
                _neuro_lib.freeSensor(self.sensor_ptr)

                self.sensor_ptr = None

    def __add_battery_callback(self):
        def __py_battery_callback(ptr, battery, user_data):
            if user_data.batteryChanged is not None:
                user_data.batteryChanged(user_data, int(battery))

        status = OpStatus()
        self.__batteryCallback = BatteryCallback(__py_battery_callback)
        self.__batteryCallbackHandle = BattPowerListenerHandle()
        _neuro_lib.addBatteryCallback(self.sensor_ptr, self.__batteryCallback, byref(self.__batteryCallbackHandle),
                                      py_object(self), byref(status))
        raise_exception_if(status)

    def __add_connection_state_callback(self):
        def __py_connection_state_callback(ptr, state, user_data):
            if user_data.sensorStateChanged is not None:
                user_data.sensorStateChanged(user_data, SensorState(state))

        status = OpStatus()
        self.__connectionStateCallback = ConnectionStateCallback(__py_connection_state_callback)
        self.__connectionStateCallbackHandle = SensorStateListenerHandle()
        _neuro_lib.addConnectionStateCallback(self.sensor_ptr, self.__connectionStateCallback,
                                              byref(self.__connectionStateCallbackHandle),
                                              py_object(self), byref(status))
        raise_exception_if(status)

    @property
    def sens_family(self) -> SensorFamily:
        status = OpStatus()
        family = _neuro_lib.getFamilySensor(self.sensor_ptr, byref(status))
        return SensorFamily(family)

    @property
    def features(self) -> [SensorFeature]:
        status = OpStatus()
        sz = _neuro_lib.getFeaturesCountSensor(self.sensor_ptr)
        sz_sensor_feature_in_out = SizeType(c_int32(sz))
        features_val = EnumType(c_int8(sz))
        _neuro_lib.getFeaturesSensor(self.sensor_ptr, features_val, sz_sensor_feature_in_out, byref(status))
        raise_exception_if(status)
        return [SensorFeature(features_val[i]) for i in range(sz_sensor_feature_in_out.contents.value)]

    @property
    def commands(self) -> [SensorCommand]:
        status = OpStatus()
        sz = _neuro_lib.getCommandsCountSensor(self.sensor_ptr)
        sz_sensor_commands_in_out = SizeType(c_int32(sz))
        commands_val = EnumType(c_int8())
        _neuro_lib.getCommandsSensor(self.sensor_ptr, commands_val, sz_sensor_commands_in_out,
                                     byref(status))
        raise_exception_if(status)
        return [SensorCommand(commands_val[i]) for i in range(sz_sensor_commands_in_out.contents.value)]

    @property
    def parameters(self) -> [ParameterInfo]:
        status = OpStatus()
        sz = _neuro_lib.getParametersCountSensor(self.sensor_ptr)
        sz_sensor_parameters_in_out = SizeType(c_int32(sz))
        parameters_val = (NativeParameterInfo * sz)()
        _neuro_lib.getParametersSensor(self.sensor_ptr, parameters_val, sz_sensor_parameters_in_out,
                                       byref(status))
        raise_exception_if(status)
        return [ParameterInfo(Param=SensorParameter(parameters_val[i].Param),
                              ParamAccess=SensorParamAccess(parameters_val[i].ParamAccess)) for i in
                range(sz_sensor_parameters_in_out.contents.value)]

    @property
    def name(self) -> str:
        status = OpStatus()
        name_out = ctypes.create_string_buffer(SENSOR_NAME_LEN)
        _neuro_lib.readNameSensor(self.sensor_ptr, name_out, SENSOR_NAME_LEN, byref(status))
        raise_exception_if(status)
        return ''.join([chr(c) for c in name_out.value]).rstrip('\x00')

    @name.setter
    def name(self, value: str):
        status = OpStatus()
        _neuro_lib.writeNameSensor(self.sensor_ptr, value.encode('utf-8'), len(value), byref(status))
        raise_exception_if(status)

    @property
    def state(self) -> SensorState:
        status = OpStatus()
        state_val = EnumType(c_int8(1))
        _neuro_lib.readStateSensor(self.sensor_ptr, state_val, byref(status))
        raise_exception_if(status)
        return SensorState(state_val.contents.value)

    @property
    def address(self) -> str:
        status = OpStatus()
        address_out = ctypes.create_string_buffer(SENSOR_ADR_LEN)
        _neuro_lib.readAddressSensor(self.sensor_ptr, address_out, SENSOR_ADR_LEN, byref(status))
        raise_exception_if(status)
        return ''.join([chr(c) for c in address_out.value]).rstrip('\x00')

    @property
    def serial_number(self) -> str:
        status = OpStatus()
        serial_number_out = ctypes.create_string_buffer(SENSOR_SN_LEN)
        _neuro_lib.readSerialNumberSensor(self.sensor_ptr, serial_number_out, SENSOR_SN_LEN, byref(status))
        raise_exception_if(status)
        return ''.join([chr(c) for c in serial_number_out.value]).rstrip('\x00')

    @serial_number.setter
    def serial_number(self, sn: str):
        status = OpStatus()
        _neuro_lib.writeSerialNumberSensor(self.sensor_ptr, sn.encode('utf-8'), len(sn), byref(status))
        raise_exception_if(status)

    @property
    def batt_power(self) -> int:
        status = OpStatus()
        power = SizeType(c_int32(1))
        _neuro_lib.readBattPowerSensor(self.sensor_ptr, power, byref(status))
        raise_exception_if(status)
        return int(power.contents.value)

    @property
    def sampling_frequency(self) -> SensorSamplingFrequency:
        if self.is_supported_parameter(SensorParameter.ParameterSamplingFrequency):
            status = OpStatus()
            sf_val = EnumType(c_int8(1))
            _neuro_lib.readSamplingFrequencySensor(self.sensor_ptr, sf_val, byref(status))
            raise_exception_if(status)
            return SensorSamplingFrequency(sf_val.contents.value)
        return SensorSamplingFrequency.FrequencyUnsupported

    @property
    def version(self) -> SensorVersion:
        status = OpStatus()
        svp = POINTER(NativeSensorVersion)
        version = svp(NativeSensorVersion())
        _neuro_lib.readVersionSensor(self.sensor_ptr, version, byref(status))
        raise_exception_if(status)
        return SensorVersion(FwMajor=int(version.contents.FwMajor),
                             FwMinor=int(version.contents.FwMinor),
                             FwPatch=int(version.contents.FwPatch),
                             HwMajor=int(version.contents.HwMajor),
                             HwMinor=int(version.contents.HwMinor),
                             HwPatch=int(version.contents.HwPatch),
                             ExtMajor=int(version.contents.ExtMajor))

    @property
    def gain(self) -> SensorGain:
        status = OpStatus()
        gain_val = EnumType(c_int8(1))
        _neuro_lib.readGainSensor(self.sensor_ptr, gain_val, byref(status))
        raise_exception_if(status)
        return SensorGain(gain_val.contents.value)

    @property
    def data_offset(self) -> SensorDataOffset:
        if self.is_supported_parameter(SensorParameter.ParameterOffset):
            status = OpStatus()
            cp = POINTER(c_uint8)
            data_offset_val = cp(c_uint8(1))
            _neuro_lib.readDataOffsetSensor(self.sensor_ptr, data_offset_val, byref(status))
            raise_exception_if(status)
            return SensorDataOffset(data_offset_val.contents.value)
        return SensorDataOffset.DataOffsetUnsupported

    @property
    def firmware_mode(self) -> SensorFirmwareMode:
        status = OpStatus()
        firmware_mode_val = EnumType(c_int8(1))
        _neuro_lib.readFirmwareModeSensor(self.sensor_ptr, firmware_mode_val, byref(status))
        raise_exception_if(status)
        return SensorFirmwareMode(firmware_mode_val.contents.value)

    def connect(self):
        """
        Device connections. After a successful connection, the sensorStateChanged callback will be called. It is a
        blocking method.

        :raises BaseException:
            If an internal error occurred while connecting.
        """
        status = OpStatus()
        _neuro_lib.connectSensor(self.sensor_ptr, byref(status))
        raise_exception_if(status)

    def disconnect(self):
        """
        Disconnect from the device. After a successful shutdown, the sensorStateChanged callback will be called

        :raises BaseException:
            If an internal error occurred while disconnecting.
        """
        status = OpStatus()
        _neuro_lib.disconnectSensor(self.sensor_ptr, byref(status))
        raise_exception_if(status)

    def is_supported_feature(self, future: SensorFeature) -> bool:
        """
        Checks if a feature is supported

        :param future:
            Feature to be checked for support
        :return: bool
            Is the feature supported or not
        """
        status = OpStatus()
        supported = _neuro_lib.isSupportedFeatureSensor(self.sensor_ptr, future.value, byref(status))
        return bool(int(supported))

    def is_supported_command(self, sensor_command: SensorCommand) -> bool:
        """
        Checks if a command is supported

        :param sensor_command:
            Command to be checked for support
        :return:
            Is the command supported or not
        """
        status = OpStatus()
        supported = _neuro_lib.isSupportedCommandSensor(self.sensor_ptr, sensor_command.value, byref(status))
        return bool(int(supported))

    def is_supported_parameter(self, sensor_parameter: SensorParameter) -> bool:
        """
        Checks if a parameter is supported

        :param sensor_parameter:
            Parameter to be checked for support
        :return:
            Is the parameter supported or not
        """
        status = OpStatus()
        supported = _neuro_lib.isSupportedParameterSensor(self.sensor_ptr, sensor_parameter.value, byref(status))
        return bool(int(supported))

    def exec_command(self, sensor_command: SensorCommand):
        """
        Sends a specific command to the device.It is a blocking method.

        :param sensor_command: SensorCommand
            Command to execute

        :raises BaseException:
            If an internal error occurred while executing command.
        """
        status = OpStatus()
        _neuro_lib.execCommandSensor(self.sensor_ptr, sensor_command.value, byref(status))
        raise_exception_if(status)
