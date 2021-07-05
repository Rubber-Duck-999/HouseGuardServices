#!/usr/bin/python3

import model
import view

class GUIController:
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