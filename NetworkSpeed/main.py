#!/usr/bin/python3
'''To set up the led array'''
import blinkt
from threading import Thread, ThreadError
import queue
import time
import logging
import os
from network_test import NetworkTest, Colours

try:
    os.remove('/home/pi/Documents/HouseGuardServices/led.log')
except:
    print("The log did not exist")

logging.basicConfig(filename='/home/pi/Documents/HouseGuardServices/led.log',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class Led:

    def __init__(self):
        self.brightness = 0.05
        self.pixels = 8
        blinkt.clear()
        blinkt.show()
        blinkt.set_clear_on_exit(True)

    def set_pixels(self, x, colour):
        red, green, blue = self.get_colours(colour)
        blinkt.set_pixel(x, red, green, blue, self.brightness)
        blinkt.show()

    def set_all(self, red, green, blue):
        for x in range(self.pixels):
            blinkt.set_pixel(x, red, green, blue, self.brightness)
        blinkt.show()

    def get_colours(self, colour):
        blue = 0
        green = 0
        red = 0
        if colour is None:
            logging.info('Colour is None')
            red = 255
            green = 192
            blue = 203
            return red, green, blue
        if colour == Colours.Red:
            red = 255
        elif colour == Colours.Orange:
            red = 236
            green = 94
            blue = 2
        elif colour == Colours.Purple:
            red = 110
            green = 51
            blue = 255
        elif colour == Colours.Green:
            green = 255
        elif colour == Colours.Blue:
            blue = 255
        return red, green, blue

    def run_lights(self, q):
        for show in Colours:
            time.sleep(5)
            red, green, blue = self.get_colours(show)
            self.set_all(red, green, blue)
        time.sleep(5)
        colour = Colours.Red
        while True:
            pixel = 0
            last_colour = colour
            try:
                colour = q.get(False)
                logging.info('New Colour: {}'.format(colour))
            except queue.Empty:
                colour = last_colour
            while pixel < self.pixels:
                self.set_all(0, 0, 0)
                self.set_pixels(pixel, colour)
                time.sleep(1)
                pixel += 1


def check_network(q):
    while True:
        network_test = NetworkTest()
        colour = Colours.Red
        if network_test.get_settings():
            colour = network_test.check_speed()
        q.put(colour)
        time.sleep(3600)


if __name__ == "__main__":
    logging.info('Starting Program')
    keyboard = False
    while not keyboard:
        try:
            q = queue.Queue()
            T1 = Thread(target=Led().run_lights, args=(q,))
            T2 = Thread(target=check_network, args=(q,))
            T1.start()
            T2.start()
            T1.join()
            T2.join()
        except KeyboardInterrupt:
            logging.error('Error occurred on keyboard')
            keyboard = True
        except ThreadError:
            logging.error('Error occurred on threads')
