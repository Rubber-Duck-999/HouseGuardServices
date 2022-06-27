#!/usr/bin/env python3

import time
import os
from colorsys import hsv_to_rgb
from unicornhatmini import UnicornHATMini
import utilities
import logging
from suntime import Sun


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

unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(0.1)
width, height = unicornhatmini.get_shape()


while True:
    hue = (time.time() / 10.0)
    r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
    unicornhatmini.set_all(r, g, b)
    unicornhatmini.show()
    time.sleep(1.0 / 60)