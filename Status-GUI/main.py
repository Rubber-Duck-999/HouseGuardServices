#!/usr/bin/python3

import tkinter as tk
 
quotes = ('A man is not complete until he is married.Then he is finished.')
 
class QuoteModel:
	def get_quote(self, n):
		try:
			value = quotes[n]
		except IndexError as err:
			value = 'Not found!'
		return value
 
class QuoteGUIView:
	def __init__(self, alarm_state):
		self.alarm_state = alarm_state
		self.window = tk.Tk()
		self.window.title("HouseGuard")

		frame3 = tk.Frame(self.window)
		frame3.pack()
		text = "Alarm State: {}".format(self.alarm_state)
		self.state_label = tk.Label(frame3, text=text)
		self.state_label.pack()

		frame4 = tk.Frame(self.window)
		frame4.pack()
		self.on_button = tk.Button(frame4, text="ON",
							width=12, command=self.on_event)
		self.off_button = tk.Button(frame4, text="OFF",
							width=12, command=self.off_event)

		self.state = False
		self.window.bind("<F11>", self.toggle_fullscreen)
		self.window.bind("<Escape>", self.end_fullscreen)
		self.set_buttons()
		self.toggle_fullscreen()

	def toggle_fullscreen(self, event=None):
		self.state = not self.state  # Just toggling the boolean
		self.window.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		self.state = False
		self.window.attributes("-fullscreen", self.state)
		return "break"

	def set_buttons(self):
		self.on_button.pack()
		self.off_button.pack()

	def on_event(self):
		print('On Button Clicked')
		self.state_label['text'] = 'Alarm State: ON'

	def off_event(self):
		print('Off Button Clicked')
		self.state_label['text'] = 'Alarm State: OFF'

class QuoteGUIController:
	def __init__(self):
		self.view = QuoteGUIView('ON')
		self.model = QuoteModel()
 
	def run(self):
		self.view.on_button.bind("<Button-1>", self.btnClicked)
		self.view.window.mainloop()
 
	def btnClicked(self,event):
		n=self.view.quoteNum.get()
		try:
			n=int(n)
		except ValueError as err:
			self.view.error("Incorrect index:"+n)
		else:
			quote = self.model.get_quote(n)
 
if __name__ == '__main__':
	controller=QuoteGUIController()
	controller.run()
