import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import db
import logging
import datetime
import time
import os
import utilities
from emailer import Emailer

filename = '/home/{}/sync/graph.log'

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

class Image:
    def __init__(self):
        self.xLabel = ''
        self.yLabel = ''
        self.title  = ''
        self.service = db.Api()
        self.x = []
        self.y = []
        self.data = []

    def clear(self):
        self.x = []
        self.y = []

    def create_images(self):
        figure(figsize = (14, 9), dpi = 60)
        plt.title(self.title)
        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)
        plt.plot(self.x, self.y)
        plt.savefig('/home/{}/sync/{}.png'.format(utilities.get_user(), self.title), dpi = 1000)

    def get_speed(self):
        speed = self.service.get_speed()
        try:
            data = speed['data']
            records = data['Records']
            for record in records:
                self.y.append(record['Download'])
                date = datetime.datetime.strptime(record['TimeOfTest'], "%a, %d %b %Y %H:%M:%S %Z")
                self.x.append(date.strftime("%H:%M"))
                time.sleep(0.5)
            self.title = "Download-Speed"
            self.xLabel = "Time (Hours)"
            self.yLabel = "Download MB/s"
            self.data.append(data['AverageDownload'])
            self.create_images()
        except KeyError as error:
            logging.error('Records do not look correct: {}'.format(error))

    def get_temp(self):
        temp = self.service.get_temperature()
        try:
            data = temp['data']
            records = data['Records']
            for record in records:
                self.y.append(record['Temperature'])
                date = datetime.datetime.strptime(record['TimeOfTemperature'], "%a, %d %b %Y %H:%M:%S %Z")
                self.x.append(date.strftime("%H:%M"))
                time.sleep(0.5)
            self.title = "Temperature"
            self.xLabel = "Time (Hours)"
            self.yLabel = "Celsius"
            self.data.append(data['AverageTemperature'])
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
    email = Emailer(image.data)
    email.get_config()
    email.send()