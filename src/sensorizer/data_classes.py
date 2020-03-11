from dataclasses import dataclass


@dataclass
class TimeserieRecord:
    """
    Class for time series
    """

    ts: float  # epoch
    data_type: str  # string(3)
    plant: str  # string(3)
    quality: float
    schema: str  # string(6)
    tag: str  # UUID
    value: float


@dataclass
class SensorConfig:
    """
    Class for sensor configuration
    """

    base_value: float  # The base of the scale for the sensor values
    sampling: float  # The sampling rate of the sensor in seconds
    number_values: int
    total_seconds: int
    model: int

    """
    TODO:
    crisis_per_hour: float
    level_changes_per_hour: float
    """


SENSOR_MODEL_RITHMIC = 1
SENSOR_MODEL_RANDOM = 2
