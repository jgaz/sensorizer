import logging
import typing
import uuid
from datetime import datetime
from typing import List, Iterator, Any

import numpy as np
from sensorizer.data_classes import SENSOR_MODEL_RITHMIC, SensorConfig, TimeserieRecord

logger = logging.getLogger()


class RealisticSensorEmulator:
    def __init__(
        self, number_of_sensors: int, start_datetime: datetime, end_datetime: datetime
    ):
        self.number_of_sensors = number_of_sensors
        if self.number_of_sensors % 10 != 0:
            raise Exception("Number of sensors must be multiple of 10")

        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    def generate_base_values(self) -> List[float]:
        """
        Generates the scale for the values of the sensors

        Returns:
            List[float] -- list of value scale per each sensor

        """
        values = []
        # TODO: This is harcoded but it could be a configuration option
        value_scales = np.array([1, 500, 1000])  # value scales
        # TODO: This is harcoded but it could be a configuration option
        # Number of sensors per value seed
        sersors_per_scale = (np.array([0.5, 0.4, 0.1]) * self.number_of_sensors).astype(
            int
        )
        scale_variation = 0.1
        for i in range(len(sersors_per_scale)):
            values.extend(
                value_scales[i]
                + (
                    np.random.random(sersors_per_scale[i])
                    * value_scales[i]
                    * scale_variation
                )
            )
        return np.array(values)

    @typing.no_type_check
    def build_sensor_list(self) -> Any:
        """
        Builds a list of sensors with its main configuration parameters:
        base value, sampling rate, total_readings and total_seconds for
        the time window

        Returns:
            List[List[float]] -- list of configuration parameters,
            1 row per sensor base_value, sampling_rate, total_readings,
            total_seconds, sensor_model
        """
        total_seconds = (self.end_datetime - self.start_datetime).total_seconds()
        base_values = self.generate_base_values()

        time_slices = np.array([1.0, 60.0, 3600.0])
        sersors_per_frequency = np.array([0.15, 0.65, 0.2]) * self.number_of_sensors

        sampling_rates = np.concatenate(
            np.array([np.ones(int(x)) for x in sersors_per_frequency]) * time_slices
        )

        total_seconds = np.ones(self.number_of_sensors) * total_seconds

        total_readings = total_seconds / sampling_rates

        # Sensor type, currently only rithmic so far
        sensor_models = np.ones(self.number_of_sensors) * SENSOR_MODEL_RITHMIC

        ret_value = list(
            zip(
                base_values,
                sampling_rates,
                total_readings,
                total_seconds,
                sensor_models,
            )
        )
        return ret_value

    def get_all_sensor_readers(
        self,
    ) -> List[Iterator[typing.Optional[TimeserieRecord]]]:

        sensor_list = self.build_sensor_list()
        sensor_configs = [SensorConfig(*c) for c in sensor_list]

        iterator = map(self.get_rithmic_reading, sensor_configs)
        return list(iterator)

    def get_rithmic_reading(
        self, sensor_config: SensorConfig
    ) -> Iterator[typing.Optional[TimeserieRecord]]:
        """
        Get sensor readings, rougly this is a sensor that oscilates slightly 10%
        around a central value.
        """
        start_time = self.start_datetime.timestamp()
        sampling = int(sensor_config.sampling)
        ts_record = TimeserieRecord(
            data_type="STD",
            plant="GRK",
            quality=100,
            schema="v0.3",
            value=0,
            tag=str(uuid.uuid1()),
            ts=datetime.now().timestamp(),
        )
        for current_second in range(int(sensor_config.total_seconds)):
            if current_second % sampling == 0:
                ts_record.value = sensor_config.base_value + (
                    np.sin(current_second * np.pi / 180)
                    * 0.1
                    * sensor_config.base_value
                )
                ts_record.ts = start_time + current_second
                yield ts_record
            else:
                yield None

    def get_random_reading(self, sensor_config: SensorConfig):
        return 0

    def transform_delay(
        self, sensor_time_serie: List[TimeserieRecord], delay: float
    ) -> List[TimeserieRecord]:
        pass

    def transform_scale(
        self, sensor_time_serie: List[TimeserieRecord], delay: float
    ) -> List[TimeserieRecord]:
        pass

    def transform_linear(
        self, sensor_time_serie: List[TimeserieRecord], delay: float
    ) -> List[TimeserieRecord]:
        pass

    def transform_failure(self, sensor_time_serie: List[TimeserieRecord]):
        pass
