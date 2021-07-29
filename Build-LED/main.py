#!/usr/bin/python3
'''To set up the led array'''
import blinkt
from threading import Thread
import queue
import time
import colorsys
from network_test import NetworkTest, Colours

class Led:

    def __init__(self):
        self.brightness = 0.05
        self.pixels = 8
        blinkt.clear()
        blinkt.show()
        blinkt.set_clear_on_exit(True)

    def set_pixels(self, x, colour):
        blue    = 0
        green   = 0
        red     = 0
        if colour == None:
            print('Colour is None')
            return
        if colour == Colours.Red:
            red   = 255
        elif colour == Colours.Purple:
            red   = 128
            blue  = 128
        elif colour == Colours.Orange:
            red   = 255
            green = 165
        elif colour == Colours.Yellow:
            red   = 245
            green = 66
        elif colour == Colours.Green:
            green = 245
        elif colour == Colours.Blue:
            blue  = 255
        blinkt.set_pixel(x, red, green, blue, self.brightness)
        blinkt.show()

    def set_all(self):
        for x in range(self.pixels):
            blinkt.set_pixel(x, 0, 0, 0, self.brightness)
        blinkt.show()

    def run_lights(self, q):
        colour = Colours.Red
        while True:
            pixel = 0
            last_colour = colour
            try:
                colour = q.get(False)
            except queue.Empty:
                colour = last_colour
            while pixel < self.pixels:
                self.set_all()
                self.set_pixels(pixel, colour)
                time.sleep(0.2)
                pixel += 1

def check_network(q):
    while True:
        network_test = NetworkTest()
        colour = network_test.check_speed()
        q.put(colour)
        time.sleep(60)


if __name__ == "__main__":
    print('Starting Program')
    q = queue.Queue()
    T1 = Thread(target=Led().run_lights, args=(q,))
    T2 = Thread(target=check_network, args=(q,))
    T1.start()
    T2.start()
    T1.join()
    T2.join()