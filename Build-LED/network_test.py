#!/usr/bin/python3

import speedtest
from datetime import datetime
import enum

class Colours(enum.Enum):
    Red    = 1
    Orange = 2
    Purple = 3
    Yellow = 4
    Green  = 5
    Blue   = 6


class NetworkTest:

    def __init__(self):
        '''Constructor for class'''
        self.speed = speedtest.Speedtest()

    def check_speed(self):
        '''Check speed of both checks'''
        red    = 25
        orange = 50
        purple = 75
        yellow = 100
        green  = 125
        blue   = 150
        down_speed = self.speed.download() / 1048576
        down = round(down_speed)
        if down <= red:
            return Colours.Red
        elif down > red and down <= orange:
            return Colours.Orange
        elif down > orange and down <= purple:
            return Colours.Purple
        elif down > orange and down <= green:
            return Colours.Yellow
        elif down > green and down <= blue:
            return Colours.Green
        else:
            return Colours.Blue

if __name__ == "__main__":
    network_test = NetworkTest()
    network_test.check_speed()
