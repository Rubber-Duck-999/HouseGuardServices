#!/usr/bin/python3
import requests
import logging

def test_request():
    try:
        response = requests.post('http://192.168.0.40:5000/motion', timeout=5)
        if response.status_code == 200:
            logging.info("Requests successful")
    except requests.ConnectionError as error:
        logging.error("Connection error: {}".format(error))
    except requests.Timeout as error:
        logging.error("Timeout on server: {}".format(error))

if __name__ == "__main__":
    test_request()