#!/usr/bin/env python3
'''
Motion script
'''
try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO
import os
import time
import logging
import logging.handlers
import datetime
import json
import requests
import subprocess

# Setup global
GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

def get_user():
    try:
        username = os.getlogin()
    except OSError:
        username = 'pi'
    return username

filename = '/home/{}/Documents/HouseGuardServices/motion.log'

try:
    name = get_user()
    filename = filename.format(name)
    os.remove(filename)
except OSError as error:
    pass

logging.basicConfig(filename=filename,
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

logging.info("Starting program")

class FileNotFound(Exception):
    '''Exception class for file checking'''

class Motion():
    '''Motion class for finding'''
    def __init__(self):
        '''Constructor'''
        self.last_detected  = ''
        self.initialised    = True
        self.server_address = ''
        self.send_data      = False
        self.path           = '/home/pi/Desktop/cam_images/'
        self.filename       = ''

    def get_settings(self):
        '''Get config env var'''
        logging.info('get_settings()')
        name = get_user()
        config_name = '/home/{}/Documents/HouseGuardServices/config.json'
        config_name = config_name.format(name)
        try:
            if not os.path.isfile(config_name):
                raise FileNotFound('File is missing')
            with open(config_name) as file:
                data = json.load(file)
            self.server_address = '{}/motion'.format(data["server_address"])
            logging.info(self.server_address)
            self.send_data = True
        except KeyError:
            logging.error("Variables not set")
        except FileNotFound:
            logging.error("File is missing")

    def motion(self):
        '''Motion detection'''
        detected = datetime.datetime.now()
        logging.info('Motion Detected: {}'.format(detected))
        if self.initialised:
            self.last_detected = datetime.datetime.now()
            logging.info('Motion First Detected')
            self.initialised = False
        else:
            delta = detected - self.last_detected
            if delta.total_seconds() > 5:
                self.last_detected = datetime.datetime.now()
                logging.info('New Motion Detected')
                self.run()
                self.publish_data()

    def publish_data(self):
        '''Send data to server if asked'''
        if self.send_data:
            try:
                files = {
                    'file': (self.filename, 
                             open(self.filename, 'rb'), 
                             'image/jpg')}
                response = requests.post(self.server_address, files=files, timeout=5)
                if response.status_code == 200:
                    logging.info("Requests successful")
                else:
                    logging.error('Requests unsuccessful')
            except requests.ConnectionError as error:
                logging.error("Connection error: {}".format(error))
            except requests.Timeout as error:
                logging.error("Timeout on server: {}".format(error))
        else:
            logging.error('Send data is off')

    def run(self):
        try:
            cmd = "raspistill -o " + self.path + "img.jpg"
            self.filename = self.path + "img.jpg"
            subprocess.call(cmd, shell=True)
            time.sleep(1)
        except FileNotFoundError:
            logging.error('File not found')

    def loop(self):
        '''Loop and wait for event'''
        logging.info('loop()')
        self.get_settings()
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
