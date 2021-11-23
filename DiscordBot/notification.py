import logging
import enum

class Notifications(enum.Enum):
    Blocked = 1
    Unknown = 2

def notify(notification, data):
    logging.info('notify()')
    messages = []
    if notification == Notifications.Blocked:
        logging.info('Blocked device')
        messages = [
            '### Blocked Device ###'
            '{} has joined the network'.format(data['Name']),
            'IP: {} && Mac: {}'.format(data['Ip'], data['Mac'])
        ]
    elif notification == Notifications.Unknown:
        logging.info('Blocked device')
        messages = [
            '### Unknown Device ###'
            '{} has joined the network'.format(data['Name']),
            'IP: {} && Mac: {}'.format(data['Ip'], data['Mac'])
        ]
    else:
        logging.error('Wrong value used')
    return messages