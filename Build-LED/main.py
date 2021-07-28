#!/usr/bin/python3
'''To set up the led array'''
import blinkt
import time
from datetime import datetime, time
import colorsys

class Led:

    def __init__(self):
        self.spacing = 360.0 / 16.0
        self.hue = 0
        blinkt.set_brightness(0.1)
        self.time_allowed = True

    def within_time(self):
        check_time = self.local.utcnow().time()
        begin_time = time(8,00)
        end_time   = time(20,00)
        begin = check_time >= begin_time
        end   = check_time <= end_time
        self.time_allowed = begin and end

    def run_lights(self):
        self.hue = int(time.time() * 100) % 360
        for x in range(8):
            offset = x * self.spacing
            h = ((self.hue + offset) % 360) / 360.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            blinkt.set_pixel(x, r, g, b)
        blinkt.show()
        time.sleep(0.001)

    def startup(self):
        while self.time_allowed:
            self.within_time()
            run_lights()

if __name__ == "__main__":
    while True:
        led = Led()
        led.startup()