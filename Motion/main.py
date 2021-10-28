#!/usr/bin/env python3
'''Motion script'''
import os
import time
import logging
import logging.handlers
import json
import requests
from camera import Camera

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
        self.server_address = ''
        self.send_data      = False
        self.filename       = ''
        self.camera = Camera()

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

    def publish_data(self):
        '''Send data to server if asked'''
        if self.send_data:
            try:
                self.filename = "{}/img.jpg".format('/home/pi/Desktop/cam_images')
                files = {
                    'image': ('img.jpg', 
                             open(self.filename, 'rb'), 
                             'image/jpg')}
                response = requests.post(self.server_address, files=files, timeout=5)
                if response.status_code == 200:
                    logging.info("Requests successful")
                    logging.info('Response: {}'.format(response))
                else:
                    logging.error('Requests unsuccessful')
            except requests.ConnectionError as error:
                logging.error("Connection error: {}".format(error))
            except requests.Timeout as error:
                logging.error("Timeout on server: {}".format(error))
        else:
            logging.error('Send data is off')

    def loop(self):
        '''Loop and wait for event'''
        logging.info('loop()')
        self.get_settings()
        logging.info('Loading hardware')
        time.sleep(2)
        logging.info('Loading Complete')
        try:
            if self.camera.run_capture():
                self.publish_data()
                time.sleep(20)
        except KeyboardInterrupt:
            logging.info('Quit')

if __name__ == "__main__":
    motion = Motion()
    motion.loop()
