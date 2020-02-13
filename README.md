# Sensorizer

A python application built in a Docker container to simulate sensor data flow to disk or event hubs, is meant
to be the starting point of a data pipeline.

The main characteristic is that it tries to simulate traffic with 
similar timings, that is, it will release up to 400K readings per second,
one by one. Then we can go for a streaming option (Azure Event Hub implemented) 
or a disk option (Avro implemented), batch the data points or not, etc... 

## Getting Started

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


## Deployment

The deployment is container based, you just need to build the docker container:
```
docker build .
```

The docker container defined in the Dockerfile will start up a process
(bin/emulate_full_plants.py) that will push the data into the configured
 queue.   

```
docker run -ti <image> /bin/bash
```

You can change the command that will run in the container by editing the file:
deploy/sensor_emulator_task.conf
 

## Built With

* Python 3.7
* Docker

## Contributing

Simply put, per branch features, merge to master, so:
- Fork the repo.
- Make a feature branch and develop.
- Test :)
- Create a pull request for your new feature.
 

