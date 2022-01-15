import requests
import logging
import json


class Api:

    def __init__(self):
        '''Constructor for API'''
        self.server = 'server'
        self.get_env()

    def get_env(self):
        logging.info('get_env()')
        config_name = '/home/pi/Documents/HouseGuardServices/config.json'
        try:
            with open(config_name) as file:
                data = json.load(file)
            self.server = data["server_address"]
        except KeyError:
            logging.error("Variables not set")
        except IOError:
            logging.error('Could not read file')

    def get(self, endpoint):
        '''Send data to server if asked'''
        data = {}
        try:
            response = requests.get(self.server + endpoint, timeout=5)
            if response.status_code == 200:
                logging.info("Requests successful")
                data = response.json()
            else:
                logging.error('Requests unsuccessful')
        except requests.ConnectionError as error:
            logging.error("Connection error: {}".format(error))
        except requests.Timeout as error:
            logging.error("Timeout on server: {}".format(error))
        return data

    def get_temperature(self):
        '''Send data to server if asked'''
        return self.get('/temp/hours/1')

    def get_motion(self):
        '''Get data to server if asked'''
        return self.get('/motion/1')

    def get_speed(self):
        '''Get data to server if asked'''
        return self.get('/network/days/1')
