#!/usr/bin/python3
'''To set up the led array'''
import blinkt
import time
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

    def set_pixels(self, colour):
        print('set_pixels()')
        blue  = 0
        green = 0
        red   = 0
        x     = x * 5
        if colour == Colours.Red:
            # Red
            red  = 220 + x
        elif colour == Colours.Yellow:
            # Yellow
            red   = 220 + x
            green = 66
        elif colour == Colours.Green:
            # Green
            green = 220 + x
        for x in range(self.pixels):
            blinkt.set_pixel(x, red, green, blue)

    def run(self, colour):
        print('run()')
        x = 0
        while x < 5:
            self.set_pixels(colour, x)
            blinkt.show()
            time.sleep(5)
            self.set_pixels(colour, x)
            blinkt.show()
            time.sleep(5)
            x += 1

    def startup(self):
        print('startup()')
        colour = self.network_test.check_speed()
        self.run(colour)


if __name__ == "__main__":
    print('Starting Program')
    led = Led()
    while True:
        led.startup()