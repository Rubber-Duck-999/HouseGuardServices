#!/usr/bin/python3
'''Python script to send emails on server'''
from datetime import datetime
import logging
import logging.handlers
import os
from state import State
from flask import Flask, request, jsonify
from validate import validate_file

app = Flask(__name__)

file = './notifier.log'

try:
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
        self.route('/motion/<int:days>', methods=['GET'])(self.get_motion)
        self.route('/motion', methods=['POST'])(self.post_motion)
        self.route('/alarm', methods=['GET'])(self.get_alarm)
        self.route('/alarm/<int:state>', methods=['POST'])(self.set_alarm)
        self.route('/temp/days/<int:days>', methods=['GET'])(self.get_temp_days)
        self.route('/temp', methods=['POST'])(self.set_temp)
        self.route('/network', methods=['POST'])(self.set_speed)
        self.route('/network/days/<int:days>', methods=['GET'])(self.get_speed)
        self.state = State()
        self.request_result = False

    def result(self):
        '''Converts bool to string'''
        logging.info('# result()')
        if self.request_result is True:
            success = "Success"
        else:
            success = "Failure"
        data = {
            "message": success
        }
        return data

    def get_motion(self, days):
        '''Motion list'''
        logging.info('# get_motion()')
        data = self.state.get_motion(days)
        events = {
            'Count': len(data),
            'Events': data
        }
        return jsonify(events)

    def post_motion(self):
        '''Create a new motion'''
        logging.info('# post_motion()')
        try:
            if request.files:
                file = request.files['image']
                logging.info('File: {}'.format(file.filename))
                if validate_file(file.filename):
                    now = datetime.now().strftime("%m-%d-%Y:%H-%M-%S") + '.jpg'
                    destination = "/".join(['/home/simon/Documents/receive', now])
                    file.save(destination)
                    request_data = {
                        'file': destination,
                        'user': request.remote_addr
                    }
                    if request_data:
                        self.request_result = self.state.add_motion(request_data)
                else:
                    logging.info('Invalid file')
            else:
                logging.error('No files attached')
        except Exception as error:
            logging.error('Error occurred on file post: {}'.format(error))
        data = self.result()
        return jsonify(data)

    def get_alarm(self):
        '''Gte a alarm message state'''
        logging.info('# get_alarm()')
        logging.info('Alarm Message received')
        state = self.state.get_state()
        events = {
            'Alarm': state
        }
        return jsonify(events)

    def set_alarm(self, state):
        logging.info('# set_alarm()')
        try:
            self.request_result = self.state.set_state(state)
        except Exception as error:
            logging.error('Error occurred on file post: {}'.format(error))
        data = self.result()
        return jsonify(data)

    def get_temp_days(self, days):
        logging.info('# get_temp_days()')
        # Ensure wrong days are not entered
        if days <= 7 and days > 0:
            logging.info('Correct days picked range: {}'.format(days))
        else:
            days = 7
        temperature, average = self.state.get_temperature(days=days)
        events = {
            'Count': len(temperature),
            'Records': temperature,
            'AverageHumidity': average[0],
            'AverageTemperature': average[1]
        }
        return jsonify(events)

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

    def get_speed(self, days):
        logging.info('# get_speed_days()')
        # Ensure wrong days are not entered
        if days <= 7 and days > 0:
            logging.info('Correct days picked range: {}'.format(days))
        else:
            days = 7
        speed, average = self.state.get_speed(days=days)
        events = {
            'Count': len(speed),
            'Records': speed,
            'AverageUpload': average[0],
            'AverageDownload': average[1]
        }
        return jsonify(events)


if __name__ == "__main__":
    logging.info("Starting program")
    server = Server(__name__)
    server.run(debug=True, host='0.0.0.0')
