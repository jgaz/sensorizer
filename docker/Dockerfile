FROM python:3.7-stretch
# apt-get and system utilities
RUN apt-get update && apt-get install -y vim supervisor
#RUN pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ sensorizer
RUN pip install sensorizer
WORKDIR /usr/src/app
COPY deploy/sensor_emulator_task.conf /etc/supervisor/conf.d/sensor_emulator_task_01.conf
COPY . .

RUN chmod +x ./entry_point.sh
CMD ["./entry_point.sh"]
