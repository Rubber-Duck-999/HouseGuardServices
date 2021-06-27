#!/usr/bin/python3
'''Python script to check too good to go api'''
import logging
from local import Emailer
from db import Database
from flask import Flask

logging.basicConfig(level=logging.INFO)
logging.info("Starting program")

app = Flask(__name__)

@app.route("/alarm/<int:state>", methods=["POST"])
def index(state):
    logging.info('Alarm Message received')
    emailer = Emailer()
    emailer.get_config()
    if state == 1:
        message = 'Alarm is now switched to: {}'.format('ON')
    else:
        message = 'Alarm is now switched to: {}'.format('OFF')
    emailer.email('Alarm has Changed', message)
    return 'Received'

@app.route("/weather/<int:temp>", methods=["POST"])
def weather(temp):
    logging.info('Weather Message received')
    logging.info(temp)
    database = Database()
    database.insert(temp)
    return 'Received'
