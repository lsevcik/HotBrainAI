from enum import Enum
from dataclasses import dataclass


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __eq__(self, other):
        if type(self).__qualname__ != type(other).__qualname__:
            return NotImplemented
        return self.name == other.name and self.value == other.value

    def __hash__(self):
        return hash((type(self).__qualname__, self.name))


class SensorFamily(OrderedEnum):
    SensorUnknown = 0
    SensorLECallibri = 1
    SensorLEKolibri = 2
    SensorLEBrainBit = 3
    SensorLEBrainBitBlack = 4


@dataclass
class SensorInfo:
    SensFamily: SensorFamily
    SensModel: int
    Name: str
    Address: str
    SerialNumber: str
    PairingRequired: bool


class SensorFeature(OrderedEnum):
    FeatureSignal = 0
    FeatureMEMS = 1
    FeatureCurrentStimulator = 2
    FeatureRespiration = 3
    FeatureResist = 4
    FeatureFPG = 5
    FeatureEnvelope = 6
    FeaturePhotoStimulator = 7
    FeatureAcousticStimulator = 8


class SensorFirmwareMode(OrderedEnum):
    ModeBootloader = 0
    ModeApplication = 1


class SensorCommand(OrderedEnum):
    CommandStartSignal = 0
    CommandStopSignal = 1
    CommandStartResist = 2
    CommandStopResist = 3
    CommandStartMEMS = 4
    CommandStopMEMS = 5
    CommandStartRespiration = 6
    CommandStopRespiration = 7
    CommandStartCurrentStimulation = 8
    CommandStopCurrentStimulation = 9
    CommandEnableMotionAssistant = 10
    CommandDisableMotionAssistant = 11
    CommandFindMe = 12
    CommandStartAngle = 13
    CommandStopAngle = 14
    CommandCalibrateMEMS = 15
    CommandResetQuaternion = 16
    CommandStartEnvelope = 17
    CommandStopEnvelope = 18
    CommandResetMotionCounter = 19
    CommandCalibrateStimulation = 20
    CommandIdle = 21
    CommandPowerDown = 22
    CommandStartFPG = 23
    CommandStopFPG = 24
    CommandStartSignalAndResist = 25
    CommandStopSignalAndResist = 26
    CommandStartPhotoStimulation = 27
    CommandStopPhotoStimulation = 28
    CommandStartAcousticStimulation = 29
    CommandStopAcousticStimulation = 30


class SensorParameter(OrderedEnum):
    ParameterName = 0
    ParameterState = 1
    ParameterAddress = 2
    ParameterSerialNumber = 3
    ParameterHardwareFilterState = 4
    ParameterFirmwareMode = 5
    ParameterSamplingFrequency = 6
    ParameterGain = 7
    ParameterOffset = 8
    ParameterExternalSwitchState = 9
    ParameterADCInputState = 10
    ParameterAccelerometerSens = 11
    ParameterGyroscopeSens = 12
    ParameterStimulatorAndMAState = 13
    ParameterStimulatorParamPack = 14
    ParameterMotionAssistantParamPack = 15
    ParameterFirmwareVersion = 16
    ParameterMEMSCalibrationStatus = 17
    ParameterMotionCounterParamPack = 18
    ParameterMotionCounter = 19
    ParameterBattPower = 20
    ParameterSensorFamily = 21
    ParameterSensorMode = 22
    ParameterIrAmplitude = 23
    ParameterRedAmplitude = 24
    ParameterEnvelopeAvgWndSz = 25
    ParameterEnvelopeDecimation = 26
    ParameterSamplingFrequencyResist = 27
    ParameterSamplingFrequencyMEMSv = 28
    ParameterSamplingFrequencyFPG = 29
    ParameterAmplifier = 30
    ParameterSensorChannels = 31
    ParameterSamplingFrequencyResp = 32


class SensorParamAccess(OrderedEnum):
    ParamAccessRead = 0
    ParamAccessReadWrite = 1
    ParamAccessReadNotify = 2


class SensorState(OrderedEnum):
    StateInRange = 0
    StateOutOfRange = 1


class SensorSamplingFrequency(OrderedEnum):
    FrequencyHz10 = 0
    FrequencyHz20 = 1
    FrequencyHz100 = 2
    FrequencyHz125 = 3
    FrequencyHz250 = 4
    FrequencyHz500 = 5
    FrequencyHz1000 = 6
    FrequencyHz2000 = 7
    FrequencyHz4000 = 8
    FrequencyHz8000 = 9
    FrequencyUnsupported = 10


class SensorGain(OrderedEnum):
    SensorGain1 = 0
    SensorGain2 = 1
    SensorGain3 = 2
    SensorGain4 = 3
    SensorGain6 = 4
    SensorGain8 = 5
    SensorGain12 = 6
    SensorGain24 = 7
    SensorGainUnsupported = 8


class SensorDataOffset(OrderedEnum):
    DataOffset0 = 0x00
    DataOffset1 = 0x01
    DataOffset2 = 0x02
    DataOffset3 = 0x03
    DataOffset4 = 0x04
    DataOffset5 = 0x05
    DataOffset6 = 0x06
    DataOffset7 = 0x07
    DataOffset8 = 0x08
    DataOffsetUnsupported = 0xFF


@dataclass
class ParameterInfo:
    Param: SensorParameter
    ParamAccess: SensorParamAccess


@dataclass
class SensorVersion:
    FwMajor: int
    FwMinor: int
    FwPatch: int
    HwMajor: int
    HwMinor: int
    HwPatch: int
    ExtMajor: int


@dataclass
class Point3D:
    X: float = 0
    Y: float = 0
    Z: float = 0


@dataclass
class MEMSData:
    PackNum: int
    Accelerometer: Point3D
    Gyroscope: Point3D


class SensorAccelerometerSensitivity(OrderedEnum):
    AccSens2g = 0
    AccSens4g = 1
    AccSens8g = 2
    AccSens16g = 3
    AccSensUnsupported = 4


class SensorGyroscopeSensitivity(OrderedEnum):
    GyroSens250Grad = 0
    GyroSens500Grad = 1
    GyroSens1000Grad = 2
    GyroSens2000Grad = 3
    GyroSensUnsupported = 4

    
@dataclass
class CallibriSignalData:
    PackNum: int
    Samples: [float]


@dataclass
class CallibriRespirationData:
    PackNum: int
    Samples: [float]


@dataclass
class CallibriEnvelopeData:
    PackNum: int
    Sample: float

    
class CallibriStimulatorState(OrderedEnum):
    StimStateNoParams = 0,
    StimStateDisabled = 1,
    StimStateEnabled = 2,
    StimStateUnsupported = 0xFF


class CallibriMotionAssistantLimb(OrderedEnum):
    MALimbRightLeg = 0,
    MALimbLeftLeg = 1,
    MALimbRightArm = 2,
    MALimbLeftArm = 3,
    MALimbUnsupported = 0xFF


class SensorFilter(OrderedEnum):
    FilterHPFBwhLvl1CutoffFreq1Hz = 0
    FilterHPFBwhLvl1CutoffFreq5Hz = 1
    FilterBSFBwhLvl2CutoffFreq45_55Hz = 2
    FilterBSFBwhLvl2CutoffFreq55_65Hz = 3
    FilterHPFBwhLvl2CutoffFreq10Hz = 4
    FilterLPFBwhLvl2CutoffFreq400H = 5


class SensorExternalSwitchInput(OrderedEnum):
    ExtSwInMioElectrodesRespUSB = 0
    ExtSwInMioElectrodes = 1
    ExtSwInMioUSB = 2
    ExtSwInRespUSB = 3


class SensorADCInput(OrderedEnum):
    ADCInputElectrodes = 0
    ADCInputShort = 1
    ADCInputTest = 2
    ADCInputResistance = 3


@dataclass
class CallibriStimulatorMAState:
    StimulatorState: CallibriStimulatorState
    MAState: CallibriStimulatorState


@dataclass
class CallibriStimulationParams:
    Current: int
    PulseWidth: int
    Frequency: int
    StimulusDuration: int


@dataclass
class CallibriMotionAssistantParams:
    GyroStart: int
    GyroStop: int
    Limb: CallibriMotionAssistantLimb
    MinPauseMs: int


@dataclass
class CallibriMotionCounterParam:
    InsenseThresholdMG: int
    InsenseThresholdSample: int


class CallibriColorType(OrderedEnum):
    CallibriColorRed = 0
    CallibriColorYellow = 1
    CallibriColorBlue = 2
    CallibriColorWhite = 3
    CallibriColorUnknown = 4


class CallibriSignalType(OrderedEnum):
    CallibriSignalTypeEEG = 0,
    CallibriSignalTypeEMG = 1,
    CallibriSignalTypeECG = 2,
    CallibriSignalTypeEDA = 3,
    CallibriSignalTypeStrainGaugeBreathing = 4,
    CallibriSignalTypeImpedanceBreathing = 5,
    CallibriSignalTypeUnknown = 6


class CallibriElectrodeState(OrderedEnum):
    ElStNormal = 0
    ElStHighResistance = 1
    ElStDetached = 2


@dataclass
class QuaternionData:
    PackNum: int
    W: float = 0
    X: float = 0
    Y: float = 0
    Z: float = 0


@dataclass
class FPGData:
    PackNum: int
    IrAmplitude: float
    RedAmplitude: float


class IrAmplitude(OrderedEnum):
    IrAmp0 = 0,
    IrAmp14 = 1,
    IrAmp28 = 2,
    IrAmp42 = 3,
    IrAmp56 = 4,
    IrAmp70 = 5,
    IrAmp84 = 6,
    IrAmp100 = 7,
    IrAmpUnsupported = 0xFF


class RedAmplitude(OrderedEnum):
    RedAmp0 = 0,
    RedAmp14 = 1,
    RedAmp28 = 2,
    RedAmp42 = 3,
    RedAmp56 = 4,
    RedAmp70 = 5,
    RedAmp84 = 6,
    RedAmp100 = 7,
    RedAmpUnsupported = 0xFF

    
@dataclass
class BrainBitSignalData:
    PackNum: int
    Marker: int
    O1: float
    O2: float
    T3: float
    T4: float


@dataclass
class BrainBitResistData:
    O1: float
    O2: float
    T3: float
    T4: float

    
class SensorAmpMode(OrderedEnum):
    Invalid = 0
    PowerDown = 1
    Idle = 2
    Signal = 3
    Resist = 4
    SignalResist = 5
