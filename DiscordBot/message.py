import logging
import json
from api import Api

class MessageManager:
    
    def __init__(self):
        logging.info('MessageManager')
        self.messages = []
        self.api = None
        self.notifications = []

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

    def create_dict(self, name, messages):
        '''Creates the template message format'''
        data = {
            'name': name,
            'messages': messages
        }
        return data

    def get_notifications(self):
        logging.info('get_notifications()')
        return self.notifications

    def get_status(self):
        logging.info('get_status()')
        status = 'Available'
        self.messages = []
        self.notifications = []
        self.get_devices()
        self.get_temperature()
        self.get_motion()
        self.get_speed()
        self.get_help()
        return status

    def get_devices(self):
        logging.info('get_devices()')
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
                    '''self.notifications.extend(
                        notify(Notifications.Blocked, device))'''
                elif device['Allowed'] == 1:
                    allowed = allowed + 1
        messages = [
            'Devices Alive: {}'.format(alive),
            'Allowed: {}'.format(allowed),
            'Blocked: {}'.format(blocked)
        ]
        data = self.create_dict('$Devices',messages)
        self.messages.append(data)

    def get_temperature(self):
        logging.info('get_temperature()')
        sensor = self.api.get_temperature()
        messages = [
            "Last Hour Temp Now: {}'C".format(round(sensor['AverageTemperature'], 2)),
            'Last Hour Humidity Now: {}%'.format(round(sensor['AverageHumidity'], 2))
        ]
        data = self.create_dict('$Sensor', messages)
        self.messages.append(data)

    def get_motion(self):
        logging.info('get_motion()')
        sensor = self.api.get_motion()
        last = sensor['Events'][sensor['Count'] - 1]['TimeOfMotion']
        messages = [
            'Last Days Total Movement: {}'.format(sensor['Count']),
            'Last Time of Movement: {}'.format(last)
        ]
        data = self.create_dict('$Movement', messages)
        self.messages.append(data)

    def get_speed(self):
        logging.info('get_speed()')
        sensor = self.api.get_speed()
        messages = [
            'Average Download: {}MB/s'.format(sensor['AverageDownload']),
            'Average Upload: {}MB/s'.format(sensor['AverageUpload'])
        ]
        data = self.create_dict('$Speed', messages)
        self.messages.append(data)

    def get_help(self):
        logging.info('get_help()')
        messages = []
        for message in self.messages:
            messages.append(message['name'])
        data = self.create_dict('$Help', messages)
        self.messages.append(data)

    def get_message(self, content):
        '''Returns list of messages'''
        logging.info('get_message()')
        for message in self.messages:
            if message['name'] == content:
                return message['messages']
        return ['Not a valid request']