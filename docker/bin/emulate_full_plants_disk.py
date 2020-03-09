import logging
import os
import sys
from datetime import datetime, timedelta
import time

from sensorizer.sensor_emulator import RealisticSensorEmulator
from sensorizer.queue_interface import QueueLocalAvro


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("You need to supply a filename for sensor output")

    number_of_sensors = os.environ.get('NUMBER_OF_SENSORS', 750000)
    number_of_hours = os.environ.get('NUMBER_OF_HOURS', 2)

    end_datetime = datetime.now()
    start_datetime = datetime.now() - timedelta(hours=number_of_hours)
    se = RealisticSensorEmulator(number_of_sensors, start_datetime=start_datetime, end_datetime=end_datetime)
    readings = se.get_all_readings()

    queue = QueueLocalAvro(sys.argv[1])

    while True and readings:
        start_time = time.time()
        empty_iterators = []
        data_points = []
        for read in readings:
            try:
                data_points.append(next(read))
            except StopIteration:
                empty_iterators.append(read)
        queue.send(data_points)

        print(f"Loop time: {time.time() - start_time}")
