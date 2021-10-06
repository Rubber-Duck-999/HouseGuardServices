#!/usr/bin/python3

import requests
import logging
import os
import json

def get_user():
    try:
        username = os.getlogin()
    except OSError:
        username = 'pi'
    return username

class FileNotFound(Exception):
    '''Exception class for file checking'''

class Model:
	def __init__(self):
		'''Constructor'''
		self.allowed = 0
		self.blocked = 0
		self.last_motion = '20 mins ago'
		self.temperature = 20
		self.server_address = ''

	def get_settings(self):
		'''Get config env var'''
		logging.info('get_settings()')
		name = get_user()
		config_name = '/home/{}/Documents/HouseGuardServices/config.json'
		config_name = config_name.format(name)
		try:
			if not os.path.isfile(config_name):
				raise FileNotFound('File is missing')
			with open(config_name) as file:
				data = json.load(file)
			self.base = '{}'.format(data["server_address"])
			logging.info(self.server_address)
			self.send_data = True
		except KeyError:
			logging.error("Variables not set")
		except FileNotFound:
			logging.error("File is missing")

	def get_data(self):
		response = None
		try:
			response = requests.post(self.server_address, timeout=5)
			if response.status_code == 200:
				logging.info("Requests successful")
			else:
				logging.error('Requests unsuccessful')
		except requests.ConnectionError as error:
			logging.error("Connection error: {}".format(error))
		except requests.Timeout as error:
			logging.error("Timeout on server: {}".format(error))
		return response

	def get_devices(self):
		base = '{}/{}'.format(self.base, 'devices')
		self.server_address = base
		response = self.get_data()
		try:
			if response:
				devices = response.json()
				self.allowed = devices['allowed']
				self.blocked = devices['blocked']
		except KeyError:
			logging.error('Devices failed')

	def get_temperature(self):
		base = '{}/{}'.format(self.base, 'weather')
		self.server_address = base
		response = self.get_data()
		try:
			if response:
				data = response.json()
				self.temperature = data['temperature']
		except KeyError:
			logging.error('Devices failed')

	def get_motion(self):
		base = '{}/{}'.format(self.base, 'motion')
		self.server_address = base
		response = self.get_data()
		try:
			if response:
				data = response.json()
				self.last_motion = data['motion']
		except KeyError:
			logging.error('Devices failed')

	def check_data(self):
		data = [
			{
				'name': 'Allowed',
				'value': self.allowed
			},
			{
				'name': 'Blocked',
				'value': self.blocked
			},
			{
				'name': 'Temperature',
				'value': self.temperature
			},
			{
				'name': 'Motion',
				'value': self.last_motion
			}
		]
		return data