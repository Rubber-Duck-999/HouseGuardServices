import datetime as dt
from datetime import timedelta
import logging
import pymongo
import json
from exceptions import BadDataError
from validate import (validate_device,
                      validate_motion,
                      validate_temperature)


class State:

    def __init__(self):
        '''Constructor for state class'''
        logging.info('# state.__init__()')
        self.client = None
        self.username = ''
        self.password = ''

    def get_settings(self):
        '''Get config env var'''
        logging.info('get_settings()')
        config_name = '/home/simon/Documents/HouseGuardServices/config.json'
        token = ''
        try:
            with open(config_name) as file:
                data = json.load(file)
            self.username = data["db_username"]
            self.password = data["db_password"]
        except KeyError:
            logging.info("Variables not set")
        except IOError:
            logging.info('Could not read file')
        return token

    def connect(self):
        logging.info('# connect()')
        self.get_settings()
        conn_str = 'mongodb://{}:{}@192.168.0.15:27017/house-guard?authSource=admin'.format(
            self.username, self.password)
        try:
            self.client = pymongo.MongoClient(
                conn_str, serverSelectionTimeoutMS=5000)
            logging.info('Success on connection')
        except pymongo.errors.OperationFailure as error:
            logging.error('Pymongo failed on auth: {}'.format(error))
        except pymongo.errors.ServerSelectionTimeoutError as error:
            logging.error('Pymongo failed on timeout: {}'.format(error))

    def get_devices(self):
        logging.info('# get_devices()')
        self.connect()
        device_list = []
        if self.client:
            try:
                local_db = self.client['house-guard']
                devices = local_db.devices
                count = 0
                for device in devices.find({}, {"_id": 0, "Name": 1, "Mac": 1, "Ip": 1, "Alive": 1, "Allowed": 1}):
                    device['Id'] = str(count)
                    device_list.append(device)
                    count = count + 1
                logging.info('Records found: {}'.format(count))
            except pymongo.errors.OperationFailure as error:
                logging.error('Pymongo failed on auth: {}'.format(error))
            except pymongo.errors.ServerSelectionTimeoutError as error:
                logging.error('Pymongo failed on timeout: {}'.format(error))
            except KeyError as error:
                logging.error("Key didn't exist on record")
        else:
            logging.error('No data could be retrieved')
        return device_list

    def add_device(self, request_data):
        logging.info('# add_device()')
        self.connect()
        success = False
        if self.client:
            try:
                data = validate_device(request_data)
                local_db = self.client['house-guard']
                devices = local_db.devices
                record = devices.insert_one(data)
                logging.info('Record Id: {}'.format(record.inserted_id))
                success = True
            except pymongo.errors.OperationFailure as error:
                logging.error('Pymongo failed on auth: {}'.format(error))
            except BadDataError as error:
                logging.error('Data was invalid')
            except pymongo.errors.ServerSelectionTimeoutError as error:
                logging.error('Pymongo failed on timeout: {}'.format(error))
            except KeyError as error:
                logging.error("Key didn't exist on record")
        else:
            logging.error('No data could be retrieved')
        return success

    def get_motion(self, days):
        '''Returns data from up to the last 7 days'''
        logging.info('# get_motion()')
        self.connect()
        motion_list = []
        if self.client:
            try:
                # Ensure wrong days are not entered
                if days <= 7 and days > 0:
                    logging.info('Correct days picked range: {}'.format(days))
                else:
                    days = 7
                local_db = self.client['house-guard']
                events = local_db.motion
                count = 0
                start = dt.datetime.now() - timedelta(days=days)
                # Querying mongo collection for motion within last 7 days
                query = {"TimeOfMotion": {
                    '$lt': dt.datetime.now(), '$gte': start}}
                for event in events.find(query, {"_id": 0, "User": 1, "TimeOfMotion": 1, "File": 1}):
                    event['Id'] = str(count)
                    motion_list.append(event)
                    count = count + 1
                # Temprorary id added for records returned in data dict
                logging.info('Records found: {}'.format(count))
            except pymongo.errors.OperationFailure as error:
                logging.error('Pymongo failed on auth: {}'.format(error))
            except pymongo.errors.ServerSelectionTimeoutError as error:
                logging.error('Pymongo failed on timeout: {}'.format(error))
            except KeyError as error:
                logging.error("Key didn't exist on record")
        else:
            logging.error('No data could be retrieved')
        return motion_list

    def add_motion(self, request_data):
        logging.info('# add_motion()')
        self.connect()
        success = False
        if self.client:
            try:
                data = validate_motion(request_data)
                local_db = self.client['house-guard']
                event = local_db.motion
                record = event.insert_one(data)
                logging.info('Record Id: {}'.format(record.inserted_id))
                success = True
            except pymongo.errors.OperationFailure as error:
                logging.error('Pymongo failed on auth: {}'.format(error))
            except BadDataError as error:
                logging.error('Data was invalid')
            except pymongo.errors.ServerSelectionTimeoutError as error:
                logging.error('Pymongo failed on timeout: {}'.format(error))
            except KeyError as error:
                logging.error("Key didn't exist on record")
        else:
            logging.error('No data could be retrieved')
        return success

    def get_state(self):
        '''Returns alarm state'''
        logging.info('# get_state()')
        self.connect()
        state = 'N/A'
        if self.client:
            try:
                local_db = self.client['house-guard']
                events = local_db.alarm
                count = 0
                for event in events.find({}, {"_id": 0, "State": 1}):
                    event['Id'] = str(count)
                    state = event['State']
                    count = count + 1
                if count > 1:
                    logging.error('Too many records found')
                # Temprorary id added for records returned in data dict
                logging.info('Records found: {}'.format(count))
            except pymongo.errors.OperationFailure as error:
                logging.error('Pymongo failed on auth: {}'.format(error))
            except pymongo.errors.ServerSelectionTimeoutError as error:
                logging.error('Pymongo failed on timeout: {}'.format(error))
            except KeyError as error:
                logging.error("Key didn't exist on record")
        else:
            logging.error('No data could be retrieved')
        return state

    def set_state(self, state):
        logging.info('# set_state()')
        self.connect()
        success = False
        if self.client:
            try:
                local_db = self.client['house-guard']
                alarm = local_db.alarm
                count = 0
                id = None
                for event in alarm.find({}, {"_id": 1, "State": 0}):
                    if count == 0:
                        id = event['_id']
                    count = count + 1
                query = {"_id": id}
                new_values = {"$set": {
                    "State": state
                }}
                record = alarm.update_one(query, new_values)
                if self.get_state() != 'N/A':
                    success = True
            except pymongo.errors.OperationFailure as error:
                logging.error('Pymongo failed on auth: {}'.format(error))
            except BadDataError as error:
                logging.error('Data was invalid')
            except pymongo.errors.ServerSelectionTimeoutError as error:
                logging.error('Pymongo failed on timeout: {}'.format(error))
            except KeyError as error:
                logging.error("Key didn't exist on record")
        else:
            logging.error('No data could be retrieved')
        return success

    def get_temperature(self, days):
        '''Returns data from up to the last 7 days'''
        logging.info('# get_temperature()')
        self.connect()
        temperature_list = []
        if self.client:
            try:
                # Ensure wrong days are not entered
                if days <= 7 and days > 0:
                    logging.info('Correct days picked range: {}'.format(days))
                else:
                    days = 7
                local_db = self.client['house-guard']
                events = local_db.temperature
                count = 0
                start = dt.datetime.now() - timedelta(days=days)
                # Querying mongo collection for motion within last 7 days
                query = {"TimeOfTemperature": {
                    '$lt': dt.datetime.now(), '$gte': start}}
                for event in events.find(query, {"_id": 0, "Temperature": 1, "TimeOfTemperature": 1, "Humidity": 1}):
                    event['Id'] = str(count)
                    temperature_list.append(event)
                    count = count + 1
                # Temprorary id added for records returned in data dict
                logging.info('Records found: {}'.format(count))
            except pymongo.errors.OperationFailure as error:
                logging.error('Pymongo failed on auth: {}'.format(error))
            except pymongo.errors.ServerSelectionTimeoutError as error:
                logging.error('Pymongo failed on timeout: {}'.format(error))
            except KeyError as error:
                logging.error("Key didn't exist on record")
        else:
            logging.error('No data could be retrieved')
        return temperature_list

    def add_temperature(self, request_data):
        logging.info('# add_temperature()')
        self.connect()
        success = False
        if self.client:
            try:
                data = validate_temperature(request_data)
                local_db = self.client['house-guard']
                temp = local_db.temperature
                record = temp.insert_one(data)
                logging.info('Record Id: {}'.format(record.inserted_id))
                success = True
            except pymongo.errors.OperationFailure as error:
                logging.error('Pymongo failed on auth: {}'.format(error))
            except BadDataError as error:
                logging.error('Data was invalid')
            except pymongo.errors.ServerSelectionTimeoutError as error:
                logging.error('Pymongo failed on timeout: {}'.format(error))
            except KeyError as error:
                logging.error("Key didn't exist on record")
        else:
            logging.error('No data could be retrieved')
        return success
