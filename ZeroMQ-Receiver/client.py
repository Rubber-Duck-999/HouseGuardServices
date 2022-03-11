#
#   Ping server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import os
import logging

file = '/home/pi/Documents/HouseGuardServices/zeromq.log'

try:
    os.remove(file)
except OSError as error:
    pass

# Add the log message handler to the logger
logging.basicConfig(filename=file,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
logging.info('Socket Binding Started')
InProgress = True

try:
    while InProgress:
        #  Wait for next request from client
        message = socket.recv()
        logging.info("Received request: %s" % message)
        #  Wait
        time.sleep(1)
        if len(message) > 1:
            InProgress = False
        #  Send reply back to client
        socket.send(b"World")
except KeyboardInterrupt as error:
    logging.error("Closing program")
