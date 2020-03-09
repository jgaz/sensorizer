import logging
import uuid
from datetime import datetime, timedelta
from typing import List

import numpy as np

from sensorizer.data_classes import TimeserieRecord


class RealisticSensorEmulator:
    oscilation = 0.01
    average: float
    crisis_per_day: float
    level_changes_per_day: float
    frequency: float

    def __init__(self, number_of_sensors: int, start_datetime: datetime, end_datetime: datetime):
        self.number_of_sensors = number_of_sensors
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    def generate_base_values(self) -> List[float]:
        if self.number_of_sensors % 10 != 0:
            raise Exception("Number of sensors must be multiple of 10")
        base_values = []
        variable_base_values = np.array([1, 500, 3600])
        chunk_sizes = (np.array([0.5, 0.4, 0.1]) * self.number_of_sensors).astype(int)

        for i in range(len(chunk_sizes)):
            base_values.append((np.random.random(chunk_sizes[i])*variable_base_values[i]*0.1)+variable_base_values[i])
        return np.array(base_values)

    def build_sensor_list(self, total_seconds: int) -> List:

        base_values = self.generate_base_values()
        base_values = np.array([item for sublist in base_values for item in sublist])

        time_slices = np.array([1.0, 60.0, 3600.0])
        frequency_distribution_count = np.array([0.15, 0.65, 0.2]) * self.number_of_sensors
        frequencies = np.array([np.ones(int(x)) for x in frequency_distribution_count]) * time_slices
        frequencies = np.array([item for sublist in frequencies for item in sublist])
        number_values = (np.ones(self.number_of_sensors) * total_seconds) / frequencies

        return list(zip(base_values, frequencies, number_values, np.ones(self.number_of_sensors) * total_seconds))

    def get_all_readings(self):

        time_window = self.end_datetime - self.start_datetime
        total_seconds = int(time_window.total_seconds())
        sensor_list = self.build_sensor_list(total_seconds)

        iterator = map(self.get_sensor_reading, sensor_list)
        return list(iterator)

    def get_sensor_reading(self, sensor_config):
        """
        return an iterator for given
        :param base_value:
        :param frequency:
        :param number_ephocs:
        :return:
        """
        base_value, frequency, _, number_ephocs = sensor_config
        start_time = self.start_datetime.timestamp()
        ephoch = 0
        frequency = int(frequency)
        ts_record = TimeserieRecord(
            data_type="STD",
            plant="GRK",
            quality=100,
            schema="v0.3",
            tag=str(uuid.uuid1()),
            value=0,
            ts=datetime.now()
        )
        for i in range(int(number_ephocs)):
            ephoch += 1
            if ephoch % frequency == 0:
                ts_record.value = base_value + (np.sin(ephoch * np.pi / 180) * 0.1 * base_value)
                ts_record.ts = start_time + ephoch
                yield ts_record

    def get_random_readings(self, start_datetime: datetime, frequency:int, base_value:float, number_values:int):
        return 0

    def transform_delay(self, sensor_time_serie: List[TimeserieRecord], delay: float) -> List[TimeserieRecord]:
        pass

    def transform_scale(self, sensor_time_serie: List[TimeserieRecord], delay: float) -> List[TimeserieRecord]:
        pass

    def transform_linear(self, sensor_time_serie: List[TimeserieRecord], delay: float) -> List[TimeserieRecord]:
        pass

    def transform_failure(self, sensor_time_serie: List[TimeserieRecord]):
        pass


