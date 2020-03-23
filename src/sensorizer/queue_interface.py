import asyncio
import dataclasses
import json
import logging
from typing import List
from azure.eventhub import EventHubClientAsync, EventData, EventHubClient
from fastavro import writer, parse_schema

from sensorizer.data_classes import TimeserieRecord


class QueueInterface:
    def send(self, events: List[TimeserieRecord]):
        pass


class QueueEventHub(QueueInterface):
    def __init__(self, address, user, key):
        self.address = address
        self.user = user
        self.key = key

        self.client_batch = EventHubClient(
            self.address, debug=False, username=self.user, password=self.key
        )
        self.sender = self.client_batch.add_sender()
        self.client_batch.run()

    def async_send(self, events: List[TimeserieRecord]):
        client = EventHubClientAsync(
            self.address, debug=True, username=self.user, password=self.key
        )

        async def run():
            sender = client.add_async_sender()
            await client.run_async()
            for event in events:
                data = EventData(str(event))
                await sender.send(data)

        loop = asyncio.get_event_loop()
        tasks = asyncio.gather(run())
        loop.run_until_complete(tasks)
        loop.run_until_complete(client.stop_async())
        loop.close()

    def batch_send(self, events: List[TimeserieRecord]):
        data = EventData(batch=[json.dumps(dataclasses.asdict(e)) for e in events])
        self.sender.transfer(data)
        self.sender.wait()

    def send(self, events: List[TimeserieRecord]):
        return self.batch_send(events)


class QueueLocalAvro(QueueInterface):
    filepath: str = ""
    counter: int = 0

    def __init__(self, filepath: str):
        self.filepath = filepath

    def send(self, events: List[TimeserieRecord]):

        schema = {
            "doc": "A sensor document",
            "name": "Sensor",
            "namespace": "equinor",
            "type": "record",
            "fields": [
                {"name": "plant", "type": "string"},
                {"name": "tag", "type": "string"},
                {"name": "value", "type": "float"},
                {"name": "timestamp", "type": "float"},
            ],
        }

        parsed_schema = parse_schema(schema)
        self.counter += len(events)
        # Writing
        with open(f"{self.filepath}/sensor.avro", "a+b") as out:
            writer(
                out,
                parsed_schema,
                [
                    {
                        "tag": e.tag,
                        "plant": e.plant,
                        "value": e.value,
                        "timestamp": e.ts,
                    }
                    for e in events
                ],
                codec="deflate",
            )
        logging.info(f"Records written: {self.counter}")
