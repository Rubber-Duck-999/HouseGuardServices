#!/usr/bin/python3
'''Python script to send emails on server'''
from datetime import datetime
import logging
import logging.handlers
import os
from state import State
from local import Emailer
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from validate import validate_file

app = Flask(__name__)

file = '/home/simon/Documents/HouseGuardServices/notifier.log'

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
        self.emailer = Emailer('simon')
        self.route('/motion/<int:days>', methods=['GET'])(self.get_motion)
        self.route('/motion', methods=['POST'])(self.post_motion)
        self.route('/alarm', methods=['GET'])(self.get_alarm)
        self.route('/alarm/<string:state>', methods=['POST'])(self.set_alarm)
        self.route('/temp/days/<int:days>', methods=['GET'])(self.get_temp_days)
        self.route('/temp/hours/<int:hours>', methods=['GET'])(self.get_temp_hours)
        self.route('/temp/minutes/<int:minutes>', methods=['GET'])(self.get_temp_minutes)
        self.route('/temp', methods=['POST'])(self.set_temp)
        self.route('/devices', methods=['POST', 'GET'])(self.devices)
        self.route('/devices/<string:alive>', methods=['PUT'])(self.devices_update)
        self.route('/network', methods=['POST'])(self.set_speed)
        self.state = State()
        self.request_result = False

    def check_config(self):
        '''REturns object email config'''
        return self.emailer.get_config()

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

    def devices(self):
        '''Devices for GET and POST'''
        logging.info('# devices()')
        logging.info('Devices received')
        result = {}
        if request.method == 'POST':
            request_data = request.get_json()
            logging.info(request_data)
            if request_data:
                self.request_result = self.state.add_device(request_data)
                self.emailer.email("New Unknown Device", request_data["Name"])
            result = self.result()
        elif request.method == 'GET':
            data = self.state.get_devices()
            result = {
                'Count': len(data),
                'Devices': data
            }
        return jsonify(result)

    def devices_update(self, alive):
        '''Edit a current device'''
        logging.info('# devices_update()')
        logging.info('Device received')
        request_data = request.get_json()
        logging.info(request_data)
        if request_data:
            self.request_result = self.state.edit_device(request_data, alive)
        return jsonify(self.result())

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
        logging.info('# alarm()')
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

    def get_temp_hours(self, hours):
        logging.info('# get_temp_hours()')
        # Ensure wrong hours are not entered
        if hours <= 23 and hours > 0:
            logging.info('Correct hours picked range: {}'.format(hours))
        else:
            hours = 23
        temperature, average = self.state.get_temperature(hours=hours)
        events = {
            'Count': len(temperature),
            'Records': temperature,
            'AverageHumidity': average[0],
            'AverageTemperature': average[1]
        }
        return jsonify(events)

    def get_temp_minutes(self, minutes):
        logging.info('# get_temp_minutes()')
        # Ensure wrong days are not entered
        if minutes <= 59 and minutes > 0:
            logging.info('Correct minutes picked range: {}'.format(minutes))
        else:
            minutes = 59
        temperature, average = self.state.get_temperature(mins=minutes)
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


if __name__ == "__main__":
    logging.info("Starting program")
    server = Server(__name__)
    if server.check_config():
        server.run(debug=True, host='0.0.0.0')
