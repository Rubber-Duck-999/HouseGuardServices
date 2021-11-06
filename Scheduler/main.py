import datetime as dt
from datetime import timedelta
import logging
import os
import pymongo
import json

filename = '/home/simon/Documents/HouseGuardServices/scheduler.log'

try:
    os.remove(filename)
except OSError as error:
    pass

# Add the log message handler to the logger
logging.basicConfig(filename=filename,
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

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
        try:
            with open(config_name) as file:
                data = json.load(file)
            self.username = data["db_username"]
            self.password = data["db_password"]
        except KeyError:
            logging.info("Variables not set")
        except IOError:
            logging.info('Could not read file')

    def connect(self):
        logging.info('# connect()')
        self.get_settings()
        conn_str = 'mongodb://{}:{}@192.168.0.15:27017/house-guard?authSource=admin'.format(self.username, self.password)
        try:
            self.client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
            logging.info('Success on connection')
        except pymongo.errors.OperationFailure as error:
            logging.error('Pymongo failed on auth: {}'.format(error))
        except pymongo.errors.ServerSelectionTimeoutError as error:
            logging.error('Pymongo failed on timeout: {}'.format(error))

    def remove_motion(self):
        '''Returns data from up to the last 5 days'''
        logging.info('# get_motion()')
        self.connect()
        success = False
        if self.client:
            try:
                local_db = self.client['house-guard']
                events = local_db.motion
                start = dt.datetime.now() -  timedelta(days=5)
                # Querying mongo collection for motion within last 5 days
                query = { "TimeOfMotion": {'$lt': start}}
                result = events.delete_many(query)
                # Temprorary id added for records returned in data dict
                logging.info('Records found: {}'.format(result))
                success = True
            except pymongo.errors.OperationFailure as error:
                logging.error('Pymongo failed on auth: {}'.format(error))
            except pymongo.errors.ServerSelectionTimeoutError as error:
                logging.error('Pymongo failed on timeout: {}'.format(error))
            except KeyError as error:
                logging.error("Key didn't exist on record")
        else:
            logging.error('No data could be retrieved')
        return success

    def remove_temperature(self):
        '''Returns data from up to the last 5 days'''
        logging.info('# get_temperature()')
        self.connect()
        success = False
        if self.client:
            try:
                local_db = self.client['house-guard']
                events = local_db.temperature
                start = dt.datetime.now() -  timedelta(days=5)
                # Querying mongo collection for temperature within last 5 days
                query = { "TimeOfTemperature": {'$lt': start}}
                result = events.delete_many(query)
                # Temprorary id added for records returned in data dict
                logging.info('Records found: {}'.format(result))
                success = True
            except pymongo.errors.OperationFailure as error:
                logging.error('Pymongo failed on auth: {}'.format(error))
            except pymongo.errors.ServerSelectionTimeoutError as error:
                logging.error('Pymongo failed on timeout: {}'.format(error))
            except KeyError as error:
                logging.error("Key didn't exist on record")
        else:
            logging.error('No data could be retrieved')
        return success

if __name__ == "__main__":
    logging.info('Starting scheduler service')
    db = State()
    db.remove_motion()
    db.remove_temperature()