#!/usr/bin/python3

import speedtest
from datetime import datetime
import enum

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

    def check_speed(self):
        '''Check speed of both checks'''
        red    = 60
        orange = 90
        purple = 120
        green  = 150
        down_speed = self.speed.download() / 1048576
        down = round(down_speed)
        if down <= red:
            return Colours.Red
        if down <= orange:
            return Colours.Orange
        if down <= purple:
            return Colours.Purple
        if down <= green:
            return Colours.Green
        return Colours.Blue

if __name__ == "__main__":
    network_test = NetworkTest()
    network_test.check_speed()
