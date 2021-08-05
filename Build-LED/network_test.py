#!/usr/bin/python3

import speedtest
from datetime import datetime
import enum


class Colours(enum.Enum):
    Red = 1
    Orange = 2
    Purple = 3
    Green = 4
    Blue = 5


class NetworkTest:

    def __init__(self):
        '''Constructor for class'''
        self.speed = speedtest.Speedtest()
        self.down = 0
        self.red = 60
        self.orange = 90
        self.purple = 120
        self.green = 150

    def check_speed(self):
        '''Check speed of both checks'''
        down = self.red
        try:
            down_speed = self.speed.download() / 1048576
            down = round(down_speed)
        except speedtest.SpeedtestException as error:
            print('Error occurred')
        if self.down != down:
            print('Speed changed: {}'.format(down))
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
