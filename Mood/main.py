#!/usr/bin/env python3

import time
import os
from colorsys import hsv_to_rgb
from unicornhatmini import UnicornHATMini
import utilities
import logging
from suntime import Sun, SunTimeException
import datetime


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


latitude = 51.86422539581071
longitude = -2.2411648453595343

sun = Sun(latitude, longitude)

# Get today's sunrise and sunset in UTC
today_sr = sun.get_local_sunrise_time()
today_ss = sun.get_local_sunset_time()
logging.info('Today at GB the sun raised at {} and get down at {} UTC'.format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))

while True:
    hue = (time.time() / 10.0)
    r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
    unicornhatmini.set_all(r, g, b)
    unicornhatmini.show()
    time.sleep(1.0 / 60)