#!/usr/bin/python3
'''Python script to send '''
# Import the email modules we'll need
import smtplib
import json
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Emailer:
    '''Emailer for houseguard'''

    def __init__(self):
        '''Constructor for class'''
        self.config_file   = '/home/pi/Documents/HouseGuardServices/config.json'
        self.from_email    = ''
        self.to_email      = ''
        self.from_password = ''
        self.last_temperature = ''

    def get_config(self):
        '''Get configuration values'''
        logging.info('# get_config()')
        try:
            if not os.path.isfile(self.config_file):
                return False
            config_file        = open(self.config_file, "r")
            config_data        = json.load(config_file)
            self.from_email    = config_data["from_email"]
            self.from_password = config_data["from_password"]
            self.to_email      = config_data["to_email"]
            self.start_temp    = config_data["start_temp"]
            return True
        except IOError as error:
            logging.error('File not available: {}'.format(error))
        except KeyError as error:
            logging.error('Key not available: {}'.format(error))
        except TypeError as error:
            logging.error('Type not available: {}'.format(error))
        return False

    def email(self, subject, text):
        '''Set up message for email from stores'''
        logging.info('# email()')
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            message = MIMEMultipart()
            message['Subject'] = subject
            message['From'] = self.from_email
            message['To'] = ", ".join(self.to_email)
            message.attach(MIMEText(text, 'plain'))
            server.login(self.from_email, self.from_password)
            print('Send email')
            server.sendmail(self.from_email, self.to_email, message.as_string())
            server.close()
        except smtplib.SMTPAuthenticationError as error:
            logging.error('Error occured on auth: {}'.format(error))
        except smtplib.SMTPException as error:
            logging.error('Error occured on SMTP: {}'.format(error))
        except TypeError as error:
            logging.error('Type error: {}'.format(error))