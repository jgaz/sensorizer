FROM python:3.7-stretch
# apt-get and system utilities
RUN apt-get update && apt-get install -y curl apt-transport-https debconf-utils vim supervisor

COPY deploy/sensor_emulator_task.conf /etc/supervisor/conf.d/sensor_emulator_task_01.conf

WORKDIR /usr/src/app
COPY sensorizer/requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN python setup.py install
RUN chmod +x deploy/create_environment.py
RUN chmod +x ./entry_point.sh
CMD ["./entry_point.sh"]