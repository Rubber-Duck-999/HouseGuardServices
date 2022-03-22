import logging
import os
import getpass
import requests
import json

def get_user():
    try:
        username = getpass.get_user()
    except OSError:
        username = 'pi'
    return username

filename = '/home/{}/sync/scheduler.log'

try:
    name = get_user()
    filename = filename.format(name)
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
        config_name = '/home/{}/sync/config.json'.format(get_user())
        try:
            with open(config_name) as file:
                data = json.load(file)
            self.username = data["db_username"]
            self.password = data["db_password"]
        except KeyError:
            logging.info("Variables not set")
        except IOError:
            logging.info('Could not read file')

    def send(self, path):
        '''Send speed to rest server'''
        try:
            url = self.server.format(path)
            response = requests.delete(url, timeout=5)
            if response.status_code == 200:
                logging.info("Requests successful")
                logging.info('Response: {}'.format(response))
            else:
                logging.error('Requests unsuccessful')
        except requests.ConnectionError as error:
            logging.error("Connection error: {}".format(error))
        except requests.Timeout as error:
            logging.error("Timeout on server: {}".format(error))
        except OSError:
            logging.error("File couldn't be removed")

if __name__ == "__main__":
    logging.info('Starting scheduler service')
    db = State()
    db.remove_temperature()
    db.remove_network()