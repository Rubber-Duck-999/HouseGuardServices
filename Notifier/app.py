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

filename = '/home/simon/Documents/HouseGuardServices/notifier.log'

try:
    os.remove(filename)
except OSError as error:
    pass

# Add the log message handler to the logger
logging.basicConfig(filename=filename,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class Server(Flask):

    def __init__(self, import_name):
        super(Server, self).__init__(import_name)
        self.emailer = Emailer('simon')
        self.route('/motion/<int:days>', methods=['GET'])(self.get_motion)
        self.route('/motion', methods=['POST'])(self.post_motion)
        self.route('/alarm', methods=['GET'])(self.get_alarm)
        self.route('/alarm/<string:state>', methods=['POST'])(self.set_alarm)
        self.route('/temp/<int:days>', methods=['GET'])(self.get_temp)
        self.route('/temp', methods=['POST'])(self.set_temp)
        self.route('/devices', methods=['POST', 'GET'])(self.devices)
        self.state = State()
        self.request_result = False

    def check_config(self):
        return self.emailer.get_config()

    def result(self):
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
        logging.info('# devices()')
        logging.info('Devices received')
        if request.method == 'POST':
            request_data = request.get_json()
            if request_data:
                self.request_result = self.state.add_device(request_data)
            data = self.result()
            return jsonify(data)
        else:
            data = self.state.get_devices()
            devices = {
                'Count': len(data),
                'Devices': data
            }
            return jsonify(devices)

    def get_motion(self, days):
        logging.info('# get_motion()')
        data = self.state.get_motion(days)
        events = {
            'Count': len(data),
            'Events': data
        }
        return jsonify(events)

    def post_motion(self):
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
                        self.request_result = self.state.add_motion(
                            request_data)
                else:
                    logging.info('Invalid file')
            else:
                logging.error('No files attached')
        except Exception as error:
            logging.error('Error occurred on file post: {}'.format(error))
        data = self.result()
        return jsonify(data)

    def get_alarm(self):
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

    def get_temp(self, days):
        logging.info('# get_temp()')
        temperature = self.state.get_temperature(days)
        events = {
            'Count': len(temperature),
            'Records': temperature
        }
        return jsonify(events)

    def set_temp(self):
        logging.info('# devices()')
        request_data = request.get_json()
        if request_data:
            self.request_result = self.state.add_temperature(request_data)
        data = self.result()
        return jsonify(data)


if __name__ == "__main__":
    logging.info("Starting program")
    server = Server(__name__)
    if server.check_config():
        server.run(debug=True, host='0.0.0.0')
