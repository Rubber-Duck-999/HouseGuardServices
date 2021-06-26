#!/usr/bin/env python3
'''
Motion script
'''

import RPi.GPIO as GPIO
import os
import time
import logging
import datetime
import json
import requests

# Setup global
GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

logging.basicConfig(level=logging.INFO)
logging.info("Starting program")

class FileNotFound(Exception):
    '''Exception class for file checking'''

class Motion():
    '''Motion class for finding'''
    def __init__(self):
        '''Constructor'''
        self.last_detected = ''
        self.initialised   = True
        self.server_address = ''
        self.send_data = False

    def get_settings(self):
        '''Get config env var'''
        logging.info('get_cpu_temperature()')
        config_name = '../config.json'
        try:
            if not os.path.isfile(config_name):
                raise FileNotFound('File is missing')
            with open(config_name) as file:
                data = json.load(file)
            self.server_address = 'http://{}'.format(data["server_address"])
            self.send_data = True
        except KeyError:
            logging.error("Variables not set")
        except FileNotFound:
            logging.error("File is missing")

    def motion(self):
        '''Motion detection'''
        detected = datetime.datetime.now()
        if self.initialised:
            self.last_detected = datetime.datetime.now()
            logging.info('Motion First Detected: {}'.format(detected))
            self.initialised = False
            return
        delta = detected - self.last_detected
        if delta.total_seconds() > 60:
            self.last_detected = datetime.datetime.now()
            logging.info('New Motion Detected: {}'.format(detected))
            self.publish_data()

    def publish_data(self):
        '''Send data to server if asked'''
        if self.send_data:
            data = {
                'motion': 1
            }
            try:
                response = requests.post(self.server_address, data=data, timeout=5)
                if response.status_code == 200:
                    logging.info("Requests successful")
            except requests.ConnectionError as error:
                logging.error("Connection error: {}".format(error))
            except requests.Timeout as error:
                logging.error("Timeout on server: {}".format(error))

    def loop(self):
        '''Loop and wait for event'''
        logging.info('loop()')
        time.sleep(2)
        try:
            GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=self.motion)
            while True:
                time.sleep(100)
        except KeyboardInterrupt:
            logging.info('Quit')
            GPIO.cleanup()

if __name__ == "__main__":
    motion = Motion()
    motion.loop()
