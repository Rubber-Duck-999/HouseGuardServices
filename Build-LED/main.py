#!/usr/bin/python3
'''To set up the led array'''
import blinkt
from threading import Thread
import time
import colorsys
from network_test import NetworkTest, Colours

colour = Colours.Red


class Led:

    def __init__(self):
        print('__init__()')
        self.brightness = 0.05
        self.pixels = 8
        blinkt.clear()
        blinkt.show()
        blinkt.set_clear_on_exit(True)

    def set_pixels(self, x):
        print('set_pixels()')
        blue    = 0
        green   = 0
        red     = 0
        if colour == None:
            print('Colour is None')
            return
        print('Colour: {}'.format(colour))
        if colour == Colours.Red:
            # Red
            red  = 255
        elif colour == Colours.Yellow:
            # Yellow
            red   = 245
            green = 66
        elif colour == Colours.Green:
            # Green
            green = 245
        blinkt.set_pixel(x, red, green, blue, self.brightness)
        blinkt.show()

    def set_all(self):
        print('set_all()')
        for x in range(self.pixels):
            blinkt.set_pixel(x, 0, 0, 0, self.brightness)
        blinkt.show()

    def run_lights(self):
        print('run_lights()')
        while True:
            pixel = 0
            while pixel < self.pixels:
                self.set_all()
                self.set_pixels(pixel)
                time.sleep(0.5)
                pixel += 1

def check_network():
    print('check_network()')
    while True:
        network_test = NetworkTest()
        colour = network_test.check_speed()
        time.sleep(10)


if __name__ == "__main__":
    print('Starting Program')
    T1 = Thread(target=Led().run_lights, args=())
    T2 = Thread(target=check_network, args=())
    T1.start()
    T2.start()
    T1.join()
    T2.join()