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
        self.brightness = 0.05
        self.time_allowed = True
        blinkt.clear()
        blinkt.show()
        blinkt.set_clear_on_exit(True)

    def within_time(self):
        check_time = self.local.utcnow().time()
        begin_time = time(8,00)
        end_time   = time(20,00)
        begin = check_time >= begin_time
        end   = check_time <= end_time
        self.time_allowed = begin and end

    def run_night(self):
        blinkt.set_all(100, 100, 100, self.brightness)
        blinkt.show()

    def run_day(self):
        self.hue = int(time.time() * 100) % 360
        for x in range(8):
            offset = x * self.spacing
            h = ((self.hue + offset) % 360) / 360.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            blinkt.set_pixel(x, r, g, self.brightness)
        blinkt.show()
        time.sleep(0.05)

    def startup(self):
        while self.time_allowed:
            self.within_time()
            run_day()
        while not self.time_allowed:
            self.within_time()
            run_night()


if __name__ == "__main__":
    while True:
        led = Led()
        led.startup()