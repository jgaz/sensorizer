from setuptools import setup, find_packages

setup(name="sensorizer", packages=find_packages())

setup(
    name='sensorizer',
    version='0.0.1',
    url='https://github.com/equinor/sensorizer',
    author='Jesus Gazol',
    author_email='jgaz@equinor.com',
    description='Timeseries data generation and preparation for batch jobs at scale',
    packages=find_packages(),
    license="GPL3"
)
