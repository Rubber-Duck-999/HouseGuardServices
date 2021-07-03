#!/usr/bin/python3

import tkinter as tk
import tkinter.ttk as ttk
import time
import random
import threading
import datetime
 
quotes = ('A man is not complete until he is married.Then he is finished.')
 
class Model:
	def __init__(self):
		'''Constructor'''

	def get_quote(self, n):
		try:
			value = quotes[n]
		except IndexError as err:
			value = 'Not found!'
		return value
 
class GUIView:
	def __init__(self, names):
		'''Constructor'''
		self.window = tk.Tk()
		self.window.title("HouseGuard")
		self.window.bind("<F11>", self.toggle_fullscreen)
		self.window.bind("<Escape>", self.end_fullscreen)
		self.state = False
		self.names = names
		self.lists = []
		self.setup_styles()
		self.setup_widgets()
		self.window.columnconfigure(0, weight=2)
		self.window.columnconfigure(1, weight=1)
		self.time_local = ''

	def setup_styles(self):
		self.style = ttk.Style()
		font = ('calibri', 24, 'bold')
		self.style.configure('TLabel',
							font=font,
							borderwidth='4')
		self.style.map('TLabel',
						foreground=[('!active', 'black')])
		self.style.configure('TButton', 
							font=font, 
							borderwidth='4')
		self.style.map('TButton', 
						foreground=[
							('active',
							'!disabled',
							'blue'),
							('!active',
							'!disabled',
							'black'),
						],
						background=[
							('active',
							'black'),
							('!active',
							'blue')
						])

	def setup_widgets(self):
		# Label widgets
		for x in range(len(self.names)):
			self.state_label = ttk.Label(text=self.names[x])
			self.state_label.grid(row=x,
								column=0,
								sticky = tk.W+tk.E,
								pady=5,
								padx=5)
		for x in range(len(self.names)):
			label = ttk.Label(text="N/A",
							justify=tk.CENTER)
			self.lists.append(label)
			self.lists[x].grid(row=x,
								column=1,
								padx=5,
								pady=5)
		self.refresh_button = ttk.Button(text="Refresh")
		self.refresh_button.grid(row=len(self.names),
								columnspan=2,
								sticky=tk.W+tk.E,
								padx=5,
								pady=5)
		self.clock = ttk.Label(text="Time",
							justify=tk.CENTER)
		row = len(self.names)+1
		self.clock.grid(row=row,
						columnspan=2,
						sticky=tk.W+tk.E,
						padx=5,
						pady=5)
		self.toggle_fullscreen()

	def toggle_fullscreen(self, event=None):
		self.state = not self.state  # Just toggling the boolean
		self.window.attributes("-fullscreen",
								self.state)
		return "break"

	def end_fullscreen(self, event=None):
		self.state = False
		self.window.attributes("-fullscreen",
								self.state)
		return "break"

	def refresh(self):
		print('Refresh Clicked')

	def set_values(self, received):
		try:
			for i in range(len(self.names)):
				if received['name'] == self.names[i]:
					label = self.lists[i]
					label['text'] = received['value']
					self.lists[i] = label
		except KeyError:
			print('Issue found on key')
		except IndexError:
			print('Issue found on index')

	def tick(self):
		# get the current local time from the PC
		time2 = time.strftime('%H:%M:%S')
		# if time string has changed, update it
		if time2 != self.time_local:
			self.time_local = time2
			self.clock.config(text=time2)
		# calls itself every 200 milliseconds
		# to update the time display as needed
		# could use >200 ms, but display gets jerky
		self.clock.after(500, self.tick)

	def check_values(self):
		for name in self.names:
			data = {
				"name": name,
				"value": random.randint(0, 20)
			}
			self.set_values(data)

class GUIController:
	def __init__(self, names):
		'''Constructor'''
		self.names = names
		self.view = GUIView(self.names)
		self.model = Model()
 
	def run(self):
		self.view.refresh_button.bind("<Button-1>", 
									self.btnClicked)
		self.view.window.bind("<<event1>>",
							self.eventhandler)
		self.view.tick()
		thd = threading.Thread(target=self.timecnt)
		# timer thread
		thd.daemon = True
		thd.start()
		self.view.window.mainloop()
 
	def btnClicked(self,event):
		self.view.check_values()

	def timecnt(self):  # runs in background thread
		print('Timer Thread',threading.get_ident())  # background thread id
		for x in range(10):
			self.view.window.event_generate("<<event1>>",
											when="tail",
											state=123) 
			# trigger event in main thread
			time.sleep(5)
			# one second

	def eventhandler(self, evt):
		# runs in main thread
		print('Event Thread',threading.get_ident())
		# event thread id (same as main)
		print(evt.state)
		# 123, data from event
		self.view.check_values()
		# update widget

if __name__ == '__main__':
	names = [
		"Temperature",
		"Humidity",
		"Alarm",
		"G2G Today",
		"Devices"
	]
	# start timer loop
	controller=GUIController(names)
	controller.run()
