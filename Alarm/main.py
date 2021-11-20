#!/usr/bin/python3

import controller
import logging
import os

def get_user():
    try:
        username = os.getlogin()
    except OSError:
        username = 'pi'
    return username

if __name__ == '__main__':
    filename = '/home/{}/Documents/HouseGuardServices/alarm.log'
    name = get_user()
    try:
        filename = filename.format(name)
        os.remove(filename)
    except OSError as error:
        pass

    # Add the log message handler to the logger
    logging.basicConfig(filename=filename,
                        format='%(asctime)s - %(levelname)s - %(message)s', 
                        level=logging.INFO)

    logging.info("Starting program")
    controller = controller.GUIController(name)
    controller.run()