#!/usr/bin/python3
'''To set up the led array'''
import blinkt
import time
import datetime
import colorsys
from network_test import NetworkTest, Colours

class Led:

    def __init__(self):
        print('__init__()')
        self.brightness = 0.1
        self.pixels = 8
        self.time_allowed = True
        self.network_test = NetworkTest()
        blinkt.clear()
        blinkt.show()
        blinkt.set_clear_on_exit(True)

    def within_time(self):
        print('within_time()')
        check_time = datetime.datetime.utcnow().time()
        begin_time = datetime.time(7,00)
        end_time   = datetime.time(20,30)
        begin = check_time >= begin_time
        end   = check_time <= end_time
        self.time_allowed = begin and end

    def run_night(self):
        print('run_night()')
        blinkt.set_all(100, 100, 100, 0.001)
        blinkt.show()
        time.sleep(30)

    def set_pixels(self):
        print('set_pixels()')
        blue  = 0
        green = 0
        red   = 0
        colour = self.network_test.check_speed()
        if colour == Colours.Red:
            # Yellow
            blue  = 245
        elif colour == Colours.Yellow:
            # Red
            red   = 245
            green = 66
        elif colour == Colours.Green:
            # Green
            green = 245
        for x in range(self.pixels):
            blinkt.set_pixel(x, red, green, blue)

    def run_day(self):
        print('run_day()')
        self.set_pixels()
        blinkt.show()
        time.sleep(30)

    def startup(self):
        print('startup()')
        self.within_time()
        while self.time_allowed:
            self.within_time()
            self.run_day()
        while not self.time_allowed:
            self.within_time()
            self.run_night()


if __name__ == "__main__":
    print('Starting Program')
    led = Led()
    while True:
        led.startup()