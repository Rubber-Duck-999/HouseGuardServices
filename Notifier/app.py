#!/usr/bin/python3
'''Python script to send emails on server'''
import logging
from local import Emailer
from db import Database
from flask import Flask, request

logging.basicConfig(level=logging.INFO)
logging.info("Starting program")

app = Flask(__name__)

@app.route("/motion", methods=["POST"])
def alarm():
    logging.info('# motion()')
    logging.info('Motion received')
    emailer = Emailer()
    emailer.get_config()
    message = 'Motion Ocurred'
    emailer.email('Motion on Alarm', message)
    return 'Received'

@app.route("/alarm/<int:state>", methods=["POST"])
def alarm(state):
    logging.info('# alarm()')
    logging.info('Alarm Message received')
    emailer = Emailer()
    emailer.get_config()
    if state == 1:
        message = 'Alarm is now switched to: {}'.format('ON')
    else:
        message = 'Alarm is now switched to: {}'.format('OFF')
    emailer.email('Alarm has Changed', message)
    return 'Received'

@app.route("/weather", methods=["POST"])
def weather():
    logging.info('# weather()')
    logging.info('Weather Message received')
    temp = request.get_json().get('temperature')
    logging.info(temp)
    #database = Database()
    #database.insert(temp)
    return 'Received'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')