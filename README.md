# Sensorizer

Sensorizer is a python library built to simulate a flow of sensor data to disk (Avro) or event hubs, is meant
to be the starting point of a data pipeline.

The library has a docker container companion so you can have a source of sensor data in approximately 5 mins,
see the docker deployment section if your sink is either an avro file or an Azure Event Hub, if you want an
additional sink, have a look at the issues section.

The main characteristic is that it tries to simulate traffic with
similar timings, that is, it will release up to 400K readings per second,
one by one. Then you can send it to a streaming sink (Azure Event Hub implemented)
or a disk option (Avro implemented).

## Docker deployment

The deployment is container based, you can just pull the container:
```
docker pull jgc31416/sensorizer:latest
```

Then pass the configuration as environment variables, set up the environment variables
depending on the sink you want, this is an example for the Avro file sink using an environment file,
see /docs folder:
```
docker run --env-file=avro_sink.cfg jgc31416/sensorizer:latest
```

You will get the generated files in the container.


### Avro file sink

You might want to map the output folder of the dump file into your container host.

```
export NUMBER_OF_SENSORS="10000"
export NUMBER_OF_HOURS="1"
export SINK_TYPE="file"                            # store sensor readings to a file
export RUNNING_MODE="batch"                        # send the readings one by one or in batch mode
export EVENT_DUMP_FILENAME="/tmp/event_dump.avro"  # Where to save the data
```


### Event Hub sink

```bash
export NUMBER_OF_SENSORS="10000"
export NUMBER_OF_HOURS="1"
export SINK_TYPE="event_hub"                       # store sensor readings to a file
export RUNNING_MODE="batch"                        # send the readings one by one or in batch mode
export EVENT_HUB_ADDRESS="amqps://<EventHubNamepace>.servicebus.windows.net/<EventHub>"
export EVENT_HUB_SAS_POLICY="<PolicyName>"
export EVENT_HUB_SAS_KEY="<SAS_KEY>"
```

### Distribution of the sensor readings

The distribution of the sensor readings is the following:

- Frequencies are: 15% 1.0s, 65% 60.0s, 20% 3600.0s (Percentage is over the number of sensors,
s is seconds per reading)
- Base reading values: 50% 1, 40% 500, 10% 1000


### Sensor format

```python
@dataclass
class TimeserieRecord:
    """
    Class for time series
    """

    ts: float  # epoch
    data_type: str  # string(3)
    plant: str  # string(3)
    quality: float
    schema: str  # string(6)
    tag: str  # UUID
    value: float
```



## Getting started with the library development

Clone the project from github and enjoy.

### Prerequisites

This software has been tested in Linux, it might work in other OSs but it
is definitely not warrantied.

```
- Ubuntu latest stable / Debian Stretch / Fedora +25
- Python 3.7 (Dataclasses and typing in the code)
- Docker (if you want a container deployment)
```

### Installing

Python requirements:

```
pip install -r requirements.txt
```


## Running the tests

As simple as:

```
pytest sensorizer/tests/
```


## Built With

* Python 3.7
* Docker

## Contributing

Simply put, per branch features, merge to master, so:
- Fork the repo.
- Make a feature branch and develop.
- Test :)
- Create a pull request for your new feature.
