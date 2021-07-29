#!/usr/bin/python3
'''To set up the led array'''
import blinkt
from threading import Thread
import time
import colorsys
from network_test import NetworkTest, Colours

class Led:

    def __init__(self):
        print('__init__()')
        self.brightness = 0.05
        self.pixels = 8
        self.network_test = NetworkTest()
        self.colour = Colours.Red
        blinkt.clear()
        blinkt.show()
        blinkt.set_clear_on_exit(True)

    def set_pixels(self, x):
        print('set_pixels()')
        blue    = 0
        green   = 0
        red     = 0
        if self.colour == Colours.Red:
            # Red
            red  = 255
        elif self.colour == Colours.Yellow:
            # Yellow
            red   = 245
            green = 66
        elif self.colour == Colours.Green:
            # Green
            green = 245
        blinkt.set_pixel(x, red, green, blue, self.brightness)
        blinkt.show()

    def run_lights(self):
        print('run_lights()')
        while True:
            pixel = 0
            while pixel < self.pixels:
                self.set_pixels(pixel)
                time.sleep(1)
                pixel += 1

    def check_network(self):
        print('check_network()')
        while True:
            self.colour = self.network_test.check_speed()
            time.sleep(10)


if __name__ == "__main__":
    print('Starting Program')
    led = Led()
    T1 = Thread(target=Led().run_lights, args=())
    T2 = Thread(target=Led().check_network, args=())
    T1.start()
    T2.start()
    T1.join()
    T2.join()