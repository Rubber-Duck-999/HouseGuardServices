from datetime import datetime
import logging
from exceptions import BadDataError

def validate_device(data):
    logging.info('validate_device()')
    device = {}
    try:
        device = {
            "Alive": True,
            "Allowed": data['Allowed'],
            "Ip": data["Ip"],
            "Mac": data['Mac'],
            "Name": data['Name']
        }
    except KeyError as error:
        logging.error('Data was not valid on keys: {}'.format(error))
        raise BadDataError('Error found on JSON Dictionary')
    return device

def validate_file(filename):
    logging.info('validate_file()')
    '''Checks file matches extensions'''
    extensions = ['png', 'jpg', 'jpeg']
    for extension in extensions:
        if extension in filename:
            return True
    return False

def validate_motion(data):
    logging.info('validate_motion()')
    motion = {}
    try:
        motion = {
            "File": data['file'],
            "TimeOfMotion": datetime.now(),
            "User": data['user']
        }
    except KeyError as error:
        logging.error('Data was not valid on keys: {}'.format(error))
        raise BadDataError('Error found on JSON Dictionary')
    return motion

def validate_temperature(data):
    logging.info('validate_temperature()')
    temp = {}
    try:
        temp = {
            "Humidity": data['humidity'],
            "TimeOfTemperature": datetime.now(),
            "Temperature": data['temp']
        }
    except KeyError as error:
        logging.error('Data was not valid on keys: {}'.format(error))
        raise BadDataError('Error found on JSON Dictionary')
    return temp

def validate_speed(data):
    logging.info('validate_speed()')
    speed = {}
    try:
        speed = {
            "Upload": data['up'],
            "Download": data['down'],
            "TimeOfTest": datetime.now(),
        }
    except KeyError as error:
        logging.error('Data was not valid on keys: {}'.format(error))
        raise BadDataError('Error found on JSON Dictionary')
    return speed