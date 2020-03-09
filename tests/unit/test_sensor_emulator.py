from datetime import datetime, timedelta

from sensorizer.sensor_emulator import RealisticSensorEmulator


class TestSensorEmulator:
    def test_generate_base_values(self):
        end_datetime = datetime.now()
        start_datetime = datetime.now() - timedelta(hours=1)
        se = RealisticSensorEmulator(
            20, start_datetime=start_datetime, end_datetime=end_datetime
        )
        results = se.generate_base_values()
        assert len(results) == 20

    def test_build_sensor_list(self):
        end_datetime = datetime.now()
        start_datetime = datetime.now() - timedelta(hours=1)
        se = RealisticSensorEmulator(
            20, start_datetime=start_datetime, end_datetime=end_datetime
        )
        results = se.build_sensor_list(3600)
        assert len(results) == 20
        assert len(results[0]) == 4

    def test_get_sensor_reading(self):
        end_datetime = datetime.now()
        start_datetime = datetime.now() - timedelta(hours=1)
        se = RealisticSensorEmulator(
            20, start_datetime=start_datetime, end_datetime=end_datetime
        )

        iterator = se.get_sensor_reading([1.0, 5, 0, 100])
        results = list(iterator)
        assert len(results) == 20
        iterator = se.get_sensor_reading([1.0, 1, 0, 100])
        results = list(iterator)
        assert len(results) == 100

    def test_get_all_readings(self):
        end_datetime = datetime.now()
        start_datetime = datetime.now() - timedelta(hours=1)
        se = RealisticSensorEmulator(
            20, start_datetime=start_datetime, end_datetime=end_datetime
        )

        readings = se.get_all_readings()

        assert len(list(readings)) == 20
