#!/usr/bin/python3
'''Python script to send emails on server'''
import logging
import logging.handlers
import os
from local import Emailer
from flask import Flask, request

filename = '/home/pi/Documents/HouseGuardServices/notifier.log'
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
        self.emailer = Emailer()
        self.route('/motion', methods=['POST'])(self.motion)
        self.route('/alarm/<int:state>', methods=['POST'])(self.alarm)
        self.route('/weather', methods=['POST'])(self.weather)
        self.alarm_state = True

    def check_config(self):
        return self.emailer.get_config()

    def motion(self):
        logging.info('# motion()')
        logging.info('Motion received')
        if self.alarm_state:
            message = 'Motion Ocurred'
            self.emailer.email('Motion on Alarm', message)
        else:
            logging.error('Alarm was offline')
        return 'Received'

    def alarm(self, state):
        logging.info('# alarm()')
        logging.info('Alarm Message received')
        if self.error_found():
            message = ''
            if state == 1:
                message = 'Alarm is now switched to: {}'.format('ON')
                self.alarm_state = True
            else:
                message = 'Alarm is now switched to: {}'.format('OFF')
                self.alarm_state = False
            self.emailer.email('Alarm has Changed', message)
        else:
            logging.error('Config was not setup')
        return 'Received'

    def weather(self):
        logging.info('# weather()')
        logging.info('Weather Message received')
        request_data = request.get_json()
        if request_data:
            logging.info(request_data)
            if 'temperature' in request_data:
                logging.info(request_data['temperature'])
        return 'Received'

if __name__ == "__main__":
    logging.info("Starting program")
    server = Server(__name__)
    if server.check_config():
        server.run(debug=True, host='0.0.0.0')