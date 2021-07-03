#!/usr/bin/python3

import controller

if __name__ == '__main__':
	names = [
		"Temperature",
		"Humidity",
		"Alarm",
		"G2G Today",
		"Devices"
	]
	# start timer loop
	controller = controller.GUIController(names)
	controller.run()
