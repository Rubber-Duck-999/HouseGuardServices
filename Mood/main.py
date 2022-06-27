#!/usr/bin/env python3

import time
import os
from colorsys import hsv_to_rgb
from unicornhatmini import UnicornHATMini
import utilities
import logging
from suntime import Sun
import datetime
import math


filename = '/home/{}/sync/mood.log'

try:
    name = utilities.get_user()
    filename = filename.format(name)
    os.remove(filename)
except OSError as error:
    pass

# Add the log message handler to the logger
logging.basicConfig(filename=filename,
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

logging.info('Starting Program')

def is_night():
    latitude = 51.86422539581071
    longitude = -2.2411648453595343
    sun = Sun(latitude, longitude)
    # Get today's sunrise and sunset in UTC
    sunrise = sun.get_local_sunrise_time()
    sunset = sun.get_local_sunset_time()

    now = datetime.now()
    if True:
        logging.info('Its night')
        return True
    return False

unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(0.1)
width, height = unicornhatmini.get_shape()


while True:
    if is_night():
        hue = (time.time() / 10.0)
        r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
        unicornhatmini.set_all(r, g, b)
        unicornhatmini.show()
        time.sleep(1.0 / 60)
    else:
        step = 0
        while x < 10000:
            step += 1

            for x in range(0, width):
                for y in range(0, height):
                    dx = (math.sin(step / width + 20) * width) + height
                    dy = (math.cos(step / height) * height) + height
                    sc = (math.cos(step / height) * height) + width

                    hue = math.sqrt(math.pow(x - dx, 2) + math.pow(y - dy, 2)) / sc
                    r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1, 1)]

                    unicornhatmini.set_pixel(x, y, r, g, b)

            unicornhatmini.show()
            time.sleep(1.0 / 60)