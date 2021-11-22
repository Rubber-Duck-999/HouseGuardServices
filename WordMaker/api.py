import requests
import logging

class Api:
    
    def __init__(self, server):
        '''Constructor for API'''
        self.server = server

    def get_words(self):
        '''Get data from server if asked'''
        word = {}
        try:
            response = requests.get('https://random-word-api.herokuapp.com/word?number=5&swear=0', timeout=5)
            if response.status_code == 200:
                logging.info("Requests successful")
                words = response.json()
            else:
                logging.error('Requests unsuccessful')
        except requests.ConnectionError as error:
            logging.error("Connection error: {}".format(error))
        except requests.Timeout as error:
            logging.error("Timeout on server: {}".format(error))
        except OSError:
            logging.error("File couldn't be removed")
        return words

    def get_meaning(self, word):
        '''Send data to server if asked'''
        data = {}
        try:
            address = 'https://api.dictionaryapi.dev/api/v2/entries/en/{}'.format(word)
            response = requests.get(address, timeout=5)
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