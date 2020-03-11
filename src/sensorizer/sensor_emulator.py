import logging
import uuid
from datetime import datetime
from typing import List

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
        Generates the base values for the list of sensors

        Returns:
            List[float] -- list of base values

        """
        values = []
        # TODO: This is harcoded but it could be a configuration option
        value_seeds = np.array([1, 500, 1000])  # values
        # TODO: This is harcoded but it could be a configuration option
        # Number of sensors per value seed
        sensors_per_seed = (np.array([0.5, 0.4, 0.1]) * self.number_of_sensors).astype(
            int
        )

        for i in range(len(sensors_per_seed)):
            values.extend(
                value_seeds[i]
                + (np.random.random(sensors_per_seed[i]) * value_seeds[i] * 0.1)
            )
        return np.array(values)

    def build_sensor_list(self, total_seconds: int) -> List[List[float]]:
        """
        Builds a list of sensors with its main configuration parameters:
        base value, sampling rate, total_readings and total_seconds for
        the time window

        Arguments:
            total_seconds {int} -- Time window lenght

        Returns:
            List[List[float]] -- list of configuration parameters,
            1 row is one sensor
        """
        base_values = self.generate_base_values()

        time_slices = np.array([1.0, 60.0, 3600.0])
        frequency_distribution_count = (
            np.array([0.15, 0.65, 0.2]) * self.number_of_sensors
        )
        sampling_rates = np.concatenate(
            np.array([np.ones(int(x)) for x in frequency_distribution_count])
            * time_slices
        )

        total_seconds = np.ones(self.number_of_sensors) * total_seconds

        total_readings = total_seconds / sampling_rates

        sensor_models = np.ones(self.number_of_sensors) * SENSOR_MODEL_RITHMIC

        return list(
            zip(
                base_values,
                sampling_rates,
                total_readings,
                total_seconds,
                sensor_models,
            )
        )

    def get_all_readings(self):
        time_window = self.end_datetime - self.start_datetime
        total_seconds = int(time_window.total_seconds())
        sensor_list = self.build_sensor_list(total_seconds)
        sensor_configs = [SensorConfig(*c) for c in sensor_list]

        iterator = map(self.get_rithmic_reading, sensor_configs)
        return list(iterator)

    def get_rithmic_reading(self, sensor_config: SensorConfig):
        start_time = self.start_datetime.timestamp()
        sampling = int(sensor_config.sampling)
        ts_record = TimeserieRecord(
            data_type="STD",
            plant="GRK",
            quality=100,
            schema="v0.3",
            tag=str(uuid.uuid1()),
            value=0,
            ts=datetime.now(),
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
