import datetime


class State:

    def __init__(self):
        self.devices = {
            'allowed': 0,
            'blocked': 0,
            'unknown': 0
        }
        self.last_motion = ''
        self.temperature = 20

    def get_devices(self):
        return self.devices

    def get_temperature(self):
        return self.temperature

    def get_motion(self):
        return self.last_motion

    def set_motion(self):
        self.last_motion = datetime.datetime.now()

    def set_devices(self, allowed, blocked, unknown):
        self.devices['allowed'] = allowed
        self.devices['blocked'] = blocked
        self.devices['unknown'] = unknown

    def set_temperature(self, temp):
        self.temperature = temp
