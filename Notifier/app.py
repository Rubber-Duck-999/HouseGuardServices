#!/usr/bin/python3
'''Python script to send emails on server'''
from datetime import datetime
import logging
import logging.handlers
import os
from state import State
from flask import Flask, request, jsonify

app = Flask(__name__)

# using getlogin() returning username

file = ''
try:
    user = os.getlogin()
    file = '/{}/sync/notifier.log'.format(user)
    os.remove(file)
except OSError as error:
    pass

# Add the log message handler to the logger
logging.basicConfig(filename=file,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class Server(Flask):

    def __init__(self, import_name):
        '''Constructor for flask API methods'''
        super(Server, self).__init__(import_name)
        self.route('/', methods=['GET'])(self.get_list)
        self.route('/temp', methods=['GET'])(self.get_temp)
        self.route('/temp', methods=['POST'])(self.set_temp)
        self.route('/network', methods=['POST'])(self.set_speed)
        self.route('/network', methods=['GET'])(self.get_speed)
        self.state = State()
        self.request_result = False

    def get_list(self):
        data = {
            "temp": [
                "GET",
                "POST"
            ],
            "network": [
                "GET",
                "POST"
            ]
        }
        return jsonify(data)

    def result(self, results=None):
        '''Converts bool to string'''
        logging.info('# result()')
        data = {
            "result": "Failure"
        }
        if self.request_result is True:
            data = {
                "result": "Success",
                "data": results
            }
        return data

    def get_temp(self):
        logging.info('# get_temp()')
        # Ensure wrong days are not entered
        self.request_result, temperature, average = self.state.get_temperature()
        results = {
            'Count': len(temperature),
            'Records': temperature,
            'AverageTemperature': average[0],
            'AverageHumidity': average[1],
        }
        data = self.result(results)
        return jsonify(data)

    def set_temp(self):
        logging.info('# set_temp()')
        request_data = request.get_json()
        if request_data:
            self.request_result = self.state.add_temperature(request_data)
        data = self.result()
        return jsonify(data)

    def set_speed(self):
        logging.info('# set_speed()')
        request_data = request.get_json()
        if request_data:
            self.request_result = self.state.add_speed(request_data)
        data = self.result()
        return jsonify(data)

    def get_speed(self):
        logging.info('# get_speed()')
        # Ensure wrong days are not entered
        self.request_result, speed, average = self.state.get_speed()
        results = {
            'Count': len(speed),
            'Records': speed,
            'AverageUpload': average[0],
            'AverageDownload': average[1]
        }
        data = self.result(results)
        return jsonify(data)


if __name__ == "__main__":
    logging.info("Starting program")
    server = Server(__name__)
    server.run(debug=True, host='0.0.0.0')
