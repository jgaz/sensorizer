from dataclasses import dataclass


@dataclass
class TimeserieRecord:
    """
    Class for time series
    """
    ts: float
    data_type: str  # 3
    plant: str  # GKR string(3)
    quality: float
    schema: str  # v0.3 string(6)
    tag: str  # 1218.13FYM0780_MAS_Y string(50)
    value: float
