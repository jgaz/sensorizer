import logging
import os
import time
from datetime import datetime, timedelta
from sensorizer import (
    SINK_TYPE_FILE,
    STORAGE_MODE_REAL_TIME,
    STORAGE_MODE_BATCH,
    SINK_TYPE_EVENT_HUB,
)
from sensorizer.sensor_emulator import RealisticSensorEmulator
from sensorizer.queue_interface import QueueInterface

debug_level = int(os.environ.get("DEBUG_LEVEL", logging.INFO))
logging.basicConfig(level=debug_level)

if __name__ == "__main__":
    sink_type = os.environ.get("SINK_TYPE") or exit("SINK_TYPE needed")
    running_mode = os.environ.get("RUNNING_MODE") or exit("RUNNING_MODE needed")
    number_of_sensors = int(os.environ.get("NUMBER_OF_SENSORS", 10000))
    number_of_hours = int(os.environ.get("NUMBER_OF_HOURS", 1))
    logging.info(
        f"# of sensors: {number_of_sensors} # hours: {number_of_hours} running mode: '{running_mode}'"
    )

    queue = QueueInterface()  # This is needed for Mypy
    if sink_type == SINK_TYPE_EVENT_HUB:
        from sensorizer.queue_interface import QueueEventHub, QueueInterface

        address = os.environ.get("EVENT_HUB_ADDRESS") or exit(
            "EVENT_HUB_ADDRESS needed"
        )
        user = os.environ.get("EVENT_HUB_SAS_POLICY") or exit(
            "EVENT_HUB_SAS_POLICY needed"
        )
        key = os.environ.get("EVENT_HUB_SAS_KEY") or exit("EVENT_HUB_SAS_KEY needed")
        queue = QueueEventHub(address, user, key)
    elif sink_type == SINK_TYPE_FILE:
        from sensorizer.queue_interface import QueueLocalAvro

        filename = os.environ.get("EVENT_DUMP_FILENAME") or exit(
            "EVENT_DUMP_FILENAME needed"
        )
        queue = QueueLocalAvro(filename)
    else:
        exit("Invalid sync type specified")

    end_datetime = datetime.now()
    start_datetime = datetime.now() - timedelta(hours=number_of_hours)
    se = RealisticSensorEmulator(
        number_of_sensors, start_datetime=start_datetime, end_datetime=end_datetime
    )
    sensor_readers = se.get_all_sensor_readers()
    process_start_time = time.time()

    while sensor_readers:
        loop_start_time = time.time()
        empty_iterators = []
        data_points = []

        for reader in sensor_readers:
            try:
                point = next(reader)
                if point:
                    data_points.append(point)
            except StopIteration:
                empty_iterators.append(reader)

        if running_mode == STORAGE_MODE_REAL_TIME:
            queue.send(data_points)
        elif running_mode == STORAGE_MODE_BATCH:
            for i in range(0, len(data_points), 10000):
                queue.batch_send(data_points[i : i + 10000])

        for iterator_to_delete in empty_iterators:
            sensor_readers.remove(iterator_to_delete)

        logging.info(
            f"""#Datapoints:{len(data_points)} #Active iterators: {len(
            sensor_readers)} Loop time: {time.time() - loop_start_time}"""
        )

    logging.info(
        f"Datapoints generated: {queue.counter} time spent: {time.time() - process_start_time}"
    )
