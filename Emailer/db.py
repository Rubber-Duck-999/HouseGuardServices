#!/usr/bin/python3
'''Python script to send to service'''
import logging
import os
import boto3
import json

class MissingSetup(Exception):
    '''Setup has not completed'''


class Database:
    '''Db interface'''

    def __init__(self, url):
        '''Constructor'''
        logging.info('# Database.__init__()')
        self.config_file = "../config.json"

    def get_config(self):
        '''Get configuration values'''
        print('# get_config()')
        try:
            if not os.path.isfile(self.config_file):
                return False
            config_file        = open(self.config_file, "r")
            config_data        = json.load(config_file)
            self.rest_api_id    = config_data["service"]["rest_api_id"]
            self.resource_id    = config_data["service"]["resource_id"]
            self.path           = config_data["service"]["path"]
            return True
        except IOError as error:
            print('File not available: {}'.format(error))
        except KeyError as error:
            print('Key not available: {}'.format(error))
        except TypeError as error:
            print('Type not available: {}'.format(error))
        return False

    def send_data(self, temp):
        '''Add record into db'''
        logging.info('# send_data()')
        data = {
            'temperature': temp
        }
        try:
            client = boto3.client('apigateway')
            response = client.test_invoke_method(
                restApiId=self.rest_api_id,
                resourceId=self.resource_id,
                httpMethod='post',
                pathWithQueryString=self.path,
                body=data
            )
            if response.status_code != 200:
                logging.error('Online post failed')
        except client.exceptions.BadRequestException as error:
            logging.error('Request failed: {}'.format(error))
        except client.exceptions.UnauthorizedException as error:
            logging.error('Request failed: {}'.format(error))
        except KeyError as error:
            logging.error('Request failed: {}'.format(error))