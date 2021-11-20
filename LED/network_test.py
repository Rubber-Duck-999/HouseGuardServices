#!/usr/bin/python3

import speedtest
import enum
import logging
import json
import requests

class Colours(enum.Enum):
    Red    = 1
    Orange = 2
    Purple = 3
    Green  = 4
    Blue   = 5


class NetworkTest:

    def __init__(self):
        '''Constructor for class'''
        self.speed = speedtest.Speedtest()
        self.down   = 0
        self.red    = 60
        self.orange = 90
        self.purple = 120
        self.green  = 150
        self.server = ''

    def get_settings(self):
        '''Get config env var'''
        logging.info('get_settings()')
        config_name = '/home/pi/Documents/HouseGuardServices/config.json'
        try:
            with open(config_name) as file:
                data = json.load(file)
            self.server = '{}/network'.format(data["server_address"])
            logging.info(self.server_address)
        except KeyError:
            logging.error("Variables not set")
        except IOError:
            logging.error("File is missing")

    def send_speed(self, down, up):
        '''Send speed to rest server'''
        try:
            data = {
                'up': up,
                'down': down,
            }
            response = requests.post(self.server, json=data, timeout=5)
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

    def check_speed(self):
        '''Check speed of both checks'''
        down = self.red
        try:
            down_speed = self.speed.download() / 1048576
            up_speed = self.speed.upload() / 1048576
            down = round(down_speed)
            up = round(up_speed)
            # self.send_speed(down, up)
        except speedtest.SpeedtestException as error:
            logging.error('Error occurred: {}'.format(error))
        if self.down != down:
            logging.info('Speed changed: {}'.format(down))
            self.down = down
        if self.down <= self.red:
            return Colours.Red
        if self.down <= self.orange:
            return Colours.Orange
        if self.down <= self.purple:
            return Colours.Purple
        if self.down <= self.green:
            return Colours.Green
        return Colours.Blue

if __name__ == "__main__":
    network_test = NetworkTest()
    network_test.check_speed()
