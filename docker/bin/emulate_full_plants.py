import logging
import os
import time
from datetime import datetime, timedelta

from sensorizer.sensor_emulator import RealisticSensorEmulator
from sensorizer.queue_interface import QueueEventHub

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    address = os.environ.get('EVENT_HUB_ADDRESS') or exit("EVENT_HUB_ADDRESS needed")
    user = os.environ.get('EVENT_HUB_SAS_POLICY') or exit('EVENT_HUB_SAS_POLICY needed')
    key = os.environ.get('EVENT_HUB_SAS_KEY') or exit('EVENT_HUB_SAS_KEY needed')
    number_of_sensors = os.environ.get('NUMBER_OF_SENSORS', 10000)
    number_of_hours = os.environ.get('NUMBER_OF_HOURS', 1)

    end_datetime = datetime.now()
    start_datetime = datetime.now() - timedelta(hours=number_of_hours)
    se = RealisticSensorEmulator(number_of_sensors, start_datetime=start_datetime, end_datetime=end_datetime)
    readings = se.get_all_readings()

    queue = QueueEventHub(address, user, key)

    while True:
        empty_iterators = []
        data_points = []
        logging.info("Getting data for batch")
        for read in readings:
            try:
                data_points.append(next(read))
            except StopIteration:
                empty_iterators.append(read)
        logging.info("Got batch data")

        for i in range(0, len(data_points), 1000):
            queue.batch_send(data_points[i:i + 1000])

        for iterator_to_delete in empty_iterators:
            readings.remove(iterator_to_delete)
        logging.info("Loop done")
