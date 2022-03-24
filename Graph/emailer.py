#!/usr/bin/python3
'''Python script to send '''
# Import the email modules we'll need
import smtplib
import json
import logging
import os
import utilities
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from datetime import date

class Emailer:
    '''Emailer for sending users their result'''

    def __init__(self, data):
        '''Constructor for class'''
        self.from_email    = ''
        self.from_password = ''
        self.html = ''
        self.user = utilities.get_user()
        self.config_file   = '/home/{}/sync/config.json'.format(self.user)
        self.data = data

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
            self.to            = config_data["to_email"]
            return True
        except IOError as error:
            logging.error('File not available: {}'.format(error))
        except KeyError as error:
            logging.error('Key not available: {}'.format(error))
        except TypeError as error:
            logging.error('Type not available: {}'.format(error))
        return False

    def html_message(self):
        logging.info('html_message()')
        today = date.today()
        temp = 'N/A'
        speed = 'N/A'
        if len(self.data) == 2:
            speed = self.data[0]
            temp  = self.data[1]
        html = '''<!DOCTYPE html>
            <html>
                <header>
                    <div style="background-color:#eee;padding:10px 20px;">
                        <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;">Daily Data - {}</h2>
                    </div>
                </header
                <body>
                    <div style="padding:20px 0px">
                        <div>
                            <h3>Statistics</h3>
                            <ul>
                                <li>Download Average - {}MB/s</li>
                                <li>Temperature Average - {}'C</li>
                            </ul>
                            <h3>Images</h3>
                            <ul>
                                <li>Network Speed - <img src="cid:speed"/></li>
                                <li>Temperature - <img src="cid:temp"/></li>
                            </ul>
                        </div>
                    </div>
                </body>
                <footer>
                    <div>
                        <p>If you liked this and wanted to know how this was developed, I have included the source code:</p>
                        <a href="https://github.com/Rubber-Duck-999/HouseGuardServices">Github</a>
                    </div>
                </footer>
            </html>
            '''.format(today, speed, temp)
        return html

    def send(self):
        '''Set up message for email from stores'''
        logging.info('# send()')
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            message = MIMEMultipart('related')
            message['Subject'] = "Daily Update - Flat 46"
            message['From'] = self.from_email
            message['To'] = self.to
            message.attach(MIMEText(self.html_message(), 'html'))
            speed = MIMEImage(open('/home/{}/sync/Download-Speed.png'.format(self.user), 'rb').read())
            temp = MIMEImage(open('/home/{}/sync/Temperature.png'.format(self.user), 'rb').read())
            speed.add_header("Content-ID", "<speed>")
            temp.add_header("Content-ID", "<temp>")
            message.attach(speed)
            message.attach(temp)
            logging.info('Attaching message')
            server.login(self.from_email, self.from_password)
            server.sendmail(self.from_email, self.to, message.as_string())
            server.close()
        except smtplib.SMTPAuthenticationError as error:
            logging.error('Error occured on auth: {}'.format(error))
        except smtplib.SMTPException as error:
            logging.error('Error occured on SMTP: {}'.format(error))
        except TypeError as error:
            logging.error('Type error on send: {}'.format(error))
        except FileNotFoundError as error:
            logging.error('File error on send: {}'.format(error))