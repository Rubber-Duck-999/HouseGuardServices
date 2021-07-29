#!/usr/bin/python3

import speedtest
from datetime import datetime
import enum

class Colours(enum.Enum):
    Red    = 1
    Yellow = 2
    Green  = 3


class NetworkTest:

    def __init__(self):
        '''Constructor for class'''
        self.speed = speedtest.Speedtest()

    def check_speed(self):
        '''Check speed of both checks'''
        low = 50
        high = 100
        down_speed = self.speed.download() / 1048576
        down = round(down_speed)
        print('Down: {}'.format(down))
        if down <= low:
            return Colours.Red
        elif down > low and down <= high:
            return Colours.Yellow
        else:
            return Colours.Green

if __name__ == "__main__":
    network_test = NetworkTest()
    network_test.check_speed()
