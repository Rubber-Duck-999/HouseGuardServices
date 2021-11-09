import logging
import json
from api import Api

class MessageManager:
    
    def __init__(self):
        logging.info('MessageManager')
        self.messages = []
        self.api = None

    def get_env(self):
        logging.info('get_env()')
        config_name = '/home/simon/Documents/HouseGuardServices/config.json'
        try:
            with open(config_name) as file:
                data = json.load(file)
            address = data["server_address"]
            self.api = Api(address)
        except KeyError:
            logging.error("Variables not set")
        except IOError:
            logging.error('Could not read file')

    def get_status(self):
        logging.info('get_status()')
        try:
            devices = self.api.get_devices()
            allowed = 0
            blocked = 0
            alive = 0
            # Get values for devices
            for device in devices['Devices']:
                if device['Alive'] == '1':
                    alive = alive + 1
                    if device['Allowed'] == 2:
                        blocked = blocked + 1
                    elif device['Allowed'] == 1:
                        allowed = allowed + 1
            # Get sensor values
            sensor = self.api.get_temperature()
            temperature = sensor['AverageTemperature']
            humidity = sensor['AverageHumidity']
            self.messages = [
                {
                    'name': '$Devices',
                    'message': 'Devices online: {}'.format(alive)
                },
                {
                    'name': '$Allowed',
                    'message': 'Allowed online: {}'.format(allowed)
                },
                {
                    'name': '$Blocked',
                    'message': 'Blocked online: {}'.format(blocked)
                },
                {
                    'name': '$Temperature',
                    'message': 'Last Hour Temp Now: {}'.format(temperature)
                },
                {
                    'name': '$Humidity',
                    'message': 'Last Hour Humidity Now: {}'.format(humidity)
                },
            ]
            logging.info(self.messages)
        except KeyError as error:
            logging.error('Key error on api: {}'.format(error))

    def get_message(self, content):
        logging.info('get_message()')
        for message in self.messages:
            if message['name'] == content:
                return message['message']
        return 'Not a valid request'