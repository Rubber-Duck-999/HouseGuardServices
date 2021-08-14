#!/usr/bin/python3

import time
import os
import logging
import json
from datetime import datetime
import boto3
import botocore
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth


def get_user():
    try:
        username = os.getlogin()
    except OSError:
        username = 'pi'
    return username


filename = '/home/{}/Documents/HouseGuardServices/alarm.log'

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

logging.info("Starting program")


class FileNotFound(Exception):
    '''Exception class for file checking'''


class Model:
    '''Class for managing requests'''

    def __init__(self):
        '''Constructor'''
        logging.info('init()')
        self.send_data = False
        self.server_address = ''
        self.auth = ''
        self.time_changed = datetime.now()

    def setup_aws(self):
        '''Setup IAM credentials'''
        try:
            self.session = boto3.Session()
            credentials = self.session.get_credentials()
            self.auth = AWSRequestsAuth(aws_access_key=credentials.access_key,
                                        aws_secret_access_key=credentials.secret_key,
                                        aws_token=credentials.token,
                                        aws_host=self.host,
                                        aws_region='eu-west-2',
                                        aws_service='execute-api')
        except botocore.exceptions.ConfigNotFound:
            logging.error('Credentials not found')

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
            self.server_address = '{}/state'.format(data["server_address"])
            self.host = data["host"]
            self.send_data = True
        except KeyError:
            logging.error("Variables not set")
        except FileNotFound:
            logging.error("File is missing")

    def check_time(self):
        self.send_data = False
        now = datetime.now()
        duration = now - self.time_changed
        seconds = duration.total_seconds()
        if seconds > 10:
            self.time_changed = now
            self.send_data = True
        return self.send_data

    def publish_data(self, state):
        '''Send data to server if asked'''
        self.get_settings()
        if self.send_data:
            data = {
                'state': state
            }
            try:
                self.setup_aws()
                response = requests.post(
                    self.server_address, json=data, timeout=5, auth=self.auth)
                if response.status_code == 200:
                    logging.info("Requests successful")
                else:
                    logging.error('Response: {}'.format(response))
            except requests.ConnectionError as error:
                logging.error("Connection error: {}".format(error))
            except requests.Timeout as error:
                logging.error("Timeout on server: {}".format(error))
