#!/usr/bin/python3

import controller

if __name__ == '__main__':
	names = [
		"Temperature",
		"Motion",
		"Allowed",
		"Blocked"
	]
	# start timer loop
	controller = controller.GUIController(names)
	controller.run()
