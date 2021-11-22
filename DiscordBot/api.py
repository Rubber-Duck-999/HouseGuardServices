import requests
import logging


class Api:

    def __init__(self, server):
        '''Constructor for API'''
        self.server = server

    def get_devices(self):
        '''Send data to server if asked'''
        devices = {}
        try:
            response = requests.get(self.server + '/devices', timeout=5)
            if response.status_code == 200:
                logging.info("Requests successful")
                devices = response.json()
            else:
                logging.error('Requests unsuccessful')
        except requests.ConnectionError as error:
            logging.error("Connection error: {}".format(error))
        except requests.Timeout as error:
            logging.error("Timeout on server: {}".format(error))
        except OSError:
            logging.error("File couldn't be removed")
        return devices

    def get_temperature(self):
        '''Send data to server if asked'''
        data = {}
        try:
            response = requests.get(self.server + '/temp/hours/1', timeout=5)
            if response.status_code == 200:
                logging.info("Requests successful")
                data = response.json()
            else:
                logging.error('Requests unsuccessful')
        except requests.ConnectionError as error:
            logging.error("Connection error: {}".format(error))
        except requests.Timeout as error:
            logging.error("Timeout on server: {}".format(error))
        except OSError:
            logging.error("File couldn't be removed")
        return data
