#!/usr/bin/python3

import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
layout = [
	[sg.Text('Welcome to the Rocket Simulator Console (2D)', size=(40, 1), font=("Helvetica", 25))],
	[sg.Text('Please enter the data from the mission to begin')],
	[sg.Text('Enter the Planet Terrain Details:', font=("Helvetica", 15))],
	[sg.Text('_' * 80)],
	[sg.ReadButton('Back', button_color=('white', 'blue')),
	sg.ReadButton('Next')]]
window = sg.Window('Rocket Simulator Console', default_element_size=(40, 1), grab_anywhere=False)
window = sg.Window('Window Title', layout, size=(800, 480))

# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
		break
	print('You entered ', event)

window.close()