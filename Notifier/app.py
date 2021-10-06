#!/usr/bin/python3
'''Python script to send emails on server'''
import logging
import logging.handlers
import os
from state import State
from local import Emailer
from flask import Flask, request


def get_user():
    try:
        username = os.getlogin()
    except OSError:
        username = 'pi'
    return username


filename = '/home/{}/Documents/HouseGuardServices/notifier.log'

try:
    name = get_user()
    filename = filename.format(name)
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
        self.emailer = Emailer(get_user())
        self.route('/motion', methods=['POST'])(self.motion)
        self.route('/alarm/<int:state>', methods=['POST'])(self.alarm)
        self.route('/weather', methods=['POST', 'GET'])(self.weather)
        self.route('/devices', methods=['POST', 'GET'])(self.devices)
        self.state = State()
        self.alarm_state = True

    def check_config(self):
        return self.emailer.get_config()

    def success_post(self):
        logging.info('# success_post()')
        return {
            "message": "Success"
        }

    def devices(self):
        logging.info('# devices()')
        logging.info('Devices received')
        if request.method == 'POST':
            request_data = request.get_json()
            if request_data:
                self.state.set_devices(request_data)
            data = self.success_post()
        else:
            self.state.get_devices()
        return data

    def motion(self):
        logging.info('# motion()')
        logging.info('Motion received')
        data = self.success_post()
        if self.alarm_state:
            uploaded_file = request.files['image']
            if uploaded_file.filename != '':
                uploaded_file.save(uploaded_file.filename)
            self.state.set_motion()
            self.emailer.email('Motion on Alarm', 'Motion Ocurred')
        else:
            logging.error('Alarm was offline')
            data = {
                'motion': self.state.get_motion()
            }
        return data

    def alarm(self, state):
        logging.info('# alarm()')
        logging.info('Alarm Message received')
        data = self.success_post()
        if state == 1:
            message = 'Alarm is now switched to: {}'.format('ON')
            self.alarm_state = True
        else:
            message = 'Alarm is now switched to: {}'.format('OFF')
            self.alarm_state = False
        self.emailer.email('Alarm has Changed', message)
        return data

    def weather(self):
        logging.info('# weather()')
        logging.info('Weather Message received')
        data = "received"
        if request.method == 'POST':
            request_data = request.get_json()
            if request_data:
                self.state.set_temperature(request_data['temperature'])
            data = self.success_post()
        else:
            data = {
                'temperature': self.state.get_temperature()
            }
        return data


if __name__ == "__main__":
    logging.info("Starting program")
    server = Server(__name__)
    if server.check_config():
        server.run(debug=True, host='0.0.0.0')
