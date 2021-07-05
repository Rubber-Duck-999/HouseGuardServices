#!/usr/bin/python3

import time
import model
import view
import threading

class GUIController:

	def __init__(self, names):
		'''Constructor'''
		self.names = names
		self.view = view.GUIView(self.names)
		self.model = model.Model()
 
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

	def timecnt(self):
		# runs in background thread
		print('Timer Thread',threading.get_ident())
		# background thread id
		x = True
		while x:
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