import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import db
import logging
import datetime
import time
from emailer import Emailer

class Image:
    def __init__(self):
        self.xLabel = ''
        self.yLabel = ''
        self.title  = ''
        self.service = db.Api()
        self.x = []
        self.y = []

    def clear(self):
        self.x = []
        self.y = []

    def create_images(self):
        figure(figsize = (14, 9), dpi = 60)
        plt.title(self.title)
        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)
        plt.plot(self.x, self.y)
        plt.savefig('/home/pi/Documents/HouseGuardServices/{}.png'.format(self.title), dpi = 1000)

    def get_speed(self):
        speed = self.service.get_speed()
        try:
            records = speed['Records']
            for record in records:
                self.y.append(record['Download'])
                date = datetime.datetime.strptime(record['TimeOfTest'], "%a, %d %b %Y %H:%M:%S %Z")
                self.x.append(date.strftime("%H:%M"))
                time.sleep(0.5)
            self.title = "Download-Speed"
            self.xLabel = "Time (Hours)"
            self.yLabel = "Download MB/s"
            self.create_images()
        except KeyError as error:
            logging.error('Records do not look correct: {}'.format(error))

    def get_temp(self):
        speed = self.service.get_temperature()
        try:
            records = speed['Records']
            for record in records:
                self.y.append(record['Temperature'])
                date = datetime.datetime.strptime(record['TimeOfTemperature'], "%a, %d %b %Y %H:%M:%S %Z")
                self.x.append(date.strftime("%H:%M"))
                time.sleep(0.5)
            self.title = "Temperature"
            self.xLabel = "Time (Hours)"
            self.yLabel = "Celsius"
            self.create_images()
        except KeyError as error:
            logging.error('Records do not look correct: {}'.format(error))

if __name__ == "__main__":
    logging.info('Starting Program')
    image = Image()
    image.clear()
    image.get_speed()
    time.sleep(4)
    image.clear()
    image.get_temp()
    email = Emailer()
    email.get_config()
    email.send()