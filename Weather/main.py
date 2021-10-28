#!/usr/bin/env python3
'''
Weather temperature script
'''

import time
import os
import logging
from subprocess import PIPE, Popen
import json
try:
    from bme280 import BME280
except ImportError:
    from mock_bme280 import BME280
import requests

def get_user():
    try:
        username = os.getlogin()
    except OSError:
        username = 'pi'
    return username

filename = '/home/{}/Documents/HouseGuardServices/weather.log'

try:
    name = get_user()
    filename = filename.format(name)
    os.remove(filename)
except OSError as error:
    pass

# Add the log message handler to the logger
logging.basicConfig(filename=filename,
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

logging.info("Starting program")

class FileNotFound(Exception):
    '''Exception class for file checking'''


class Temperature:
    '''Class for managing system and node temp'''
    SECONDS_PER_MINUTE = 60

    def __init__(self):
        '''Constructor'''
        logging.info('init()')
        # BME280 temperature/pressure/humidity sensor
        # Tuning factor for compensation. Decrease this number to adjust the
        # temperature down, and increase to adjust up
        self.factor     = 1
        self.bme280     = BME280()
        self.send_data  = False
        # Default of 10 minutes
        self.wait_time      = 10 * Temperature.SECONDS_PER_MINUTE
        self.server_address = ''
        self.temperature    = 0.0
        self.humidity       = 0.0

    def get_settings(self):
        '''Get config env var'''
        logging.info('get_cpu_temperature()')
        name = get_user()
        config_name = '/home/{}/Documents/HouseGuardServices/config.json'
        config_name = config_name.format(name)
        try:
            if not os.path.isfile(config_name):
                raise FileNotFound('File is missing')
            with open(config_name) as file:
                data = json.load(file)
            self.wait_time      = data["weather_wait_time"]
            self.server_address = '{}/temp'.format(data["server_address"])
            self.factor         = data["temperature_factor"]
            self.send_data = True
        except KeyError:
            logging.error("Variables not set")
        except FileNotFound:
            logging.error("File is missing")

    def get_cpu_temperature(self):
        '''Get the temperature of the CPU for compensation'''
        logging.info('get_cpu_temperature()')
        cpu_temp = 0.0
        try:
            process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
            output, _error = process.communicate()
            if process.returncode != 0:
                logging.error("Vcgencmd failed")
            else:
                cpu_temp = float(output[output.index('=') + 1:output.rindex("'")])
        except FileNotFoundError:
            logging.error('Mocking as not found')
        return cpu_temp

    def get_sensor_temperature(self):
        '''Grab the bme280 temp'''
        logging.info('get_sensor_temperature()')
        cpu_temp = self.get_cpu_temperature()
        logging.info('CPU Temp: {}'.format(cpu_temp))
        raw_temp = self.bme280.get_temperature()
        logging.info('Raw Temp: {}'.format(raw_temp))
        self.temperature = raw_temp - ((cpu_temp - raw_temp) / self.factor)
        logging.info("Temperature: {:.2f}'C".format(self.temperature))
        self.temperature = round(self.temperature, 1)

    def publish_data(self):
        '''Send data to server if asked'''
        if self.send_data:
            data = {
                'temp': self.temperature,
                'humidity': self.bme280.get_humidity()
            }
            try:
                response = requests.post(self.server_address, json=data, timeout=5)
                if response.status_code == 200:
                    logging.info("Requests successful")
                else:
                    logging.error('Response: {}'.format(response))
            except requests.ConnectionError as error:
                logging.error("Connection error: {}".format(error))
            except requests.Timeout as error:
                logging.error("Timeout on server: {}".format(error))

    def loop(self):
        '''Loop through sensor and publish'''
        self.get_settings()
        while True:
            self.get_sensor_temperature()
            self.publish_data()
            time.sleep(4 * self.wait_time)

if __name__ == "__main__":
    temp = Temperature()
    temp.loop()
