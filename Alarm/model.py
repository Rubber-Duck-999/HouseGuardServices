#!/usr/bin/python3

import os
import logging
import json
from datetime import datetime
import requests


class FileNotFound(Exception):
    '''Exception class for file checking'''


class Model:
    '''Class for managing requests'''
    def __init__(self, name):
        '''Constructor'''
        logging.info('init()')
        self.server_address = ''
        self.auth           = ''
        self.time_changed   = datetime.now()
        self.state = 'ON'
        self.name = name

    def get_settings(self):
        '''Get config env var'''
        logging.info('get_settings()')
        config_name = '/home/{}/Documents/HouseGuardServices/config.json'
        config_name = config_name.format(self.name)
        try:
            if not os.path.isfile(config_name):
                raise FileNotFound('File is missing')
            with open(config_name) as file:
                data = json.load(file)
            self.server_address = '{}/alarm'.format(data["server_address"])
        except KeyError:
            logging.error("Variables not set")
        except FileNotFound:
            logging.error("File is missing")

    def set_data(self, state):
        self.state = state

    def publish_data(self):
        '''Send data to server if asked'''
        try:
            address = "{}/{}".format(self.server_address, self.state)
            response = requests.post(address, timeout=5)
            if response.status_code == 200:
                logging.info("Requests successful")
            else:
                logging.error('Response: {}'.format(response))
        except requests.ConnectionError as error:
            logging.error("Connection error: {}".format(error))
        except requests.Timeout as error:
            logging.error("Timeout on server: {}".format(error))