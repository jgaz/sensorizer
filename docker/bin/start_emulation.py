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

debug_level = int(os.environ.get("DEBUG_LEVEL", logging.INFO))
logging.basicConfig(level=debug_level)

if __name__ == "__main__":
    sink_type = os.environ.get("SINK_TYPE") or exit("SINK_TYPE needed")
    running_mode = os.environ.get("RUNNING_MODE") or exit("RUNNING_MODE needed")
    number_of_sensors = int(os.environ.get("NUMBER_OF_SENSORS", 100))
    number_of_hours = int(os.environ.get("NUMBER_OF_HOURS", 1))
    logging.info(
        f"# of sensors: {number_of_sensors} # hours: {number_of_hours} running mode: '{running_mode}'"
    )

    if sink_type == SINK_TYPE_EVENT_HUB:
        from sensorizer.queue_interface import QueueEventHub

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
            "EVENT_HUB_SAS_POLICY needed"
        )
        queue = QueueLocalAvro(filename)
    else:
        exit("Invalid sync type specified")

    end_datetime = datetime.now()
    start_datetime = datetime.now() - timedelta(hours=number_of_hours)
    se = RealisticSensorEmulator(
        number_of_sensors, start_datetime=start_datetime, end_datetime=end_datetime
    )
    readings = se.get_all_readings()
    process_start_time = time.time()
    while readings:
        loop_start_time = time.time()
        empty_iterators = []
        data_points = []

        for read in readings:
            try:
                data_points.append(next(read))
            except StopIteration:
                empty_iterators.append(read)

        if running_mode == STORAGE_MODE_REAL_TIME:
            queue.send(data_points)
        elif running_mode == STORAGE_MODE_BATCH:
            for i in range(0, len(data_points), 1000):
                queue.batch_send(data_points[i : i + 1000])
        for iterator_to_delete in empty_iterators:
            readings.remove(iterator_to_delete)
        logging.debug(
            f"""#Datapoints:{len(data_points)} #Iterators to delete: {len(
            empty_iterators)} Loop time: {time.time() - loop_start_time}"""
        )

    logging.info(
        f"Datapoints generated: {queue.counter} time spent: {time.time() - process_start_time}"
    )
