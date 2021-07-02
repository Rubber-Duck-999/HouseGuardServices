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
    def __init__(self):
        self.window = tk.Tk()
                 self.window.title("Celebrity Quotes Selector")
 
        frame1 = tk.Frame(self.window)
        frame1.pack()
                 tk.Label(frame1, text="Please enter the index of the famous quote you want to find? ").pack(side="left")
                 self.quoteNum = tk.StringVar() # Quote index
        tk.Entry(frame1, textvariable=self.quoteNum, justify="right").pack(side="left")
                 self.btn = tk.Button(frame1, text="query")
        self.btn.pack(side="left")
 
        frame2 = tk.Frame(self.window)
        frame2.pack()
                 self.quoteText = tk.StringVar() # Quote text
        tk.Label(frame2, textvariable=self.quoteText).pack()
 
    def error(self,msg):
        self.quoteText.set('Error:{}'.format(msg))
 
    def show(self, quote):
        self.quoteText.set('And the quote is:"{}"'.format(quote))
 
class QuoteGUIController:
    def __init__(self):
        self.view = QuoteGUIView()
        self.model = QuoteModel()
 
    def run(self):
        self.view.btn.bind("<Button-1>", self.btnClicked)
        self.view.window.mainloop()
 
    def btnClicked(self,event):
        n=self.view.quoteNum.get()
        try:
            n=int(n)
        except ValueError as err:
            self.view.error("Incorrect index:"+n)
        else:
            quote = self.model.get_quote(n)
            self.view.show(quote)
 
if __name__ == '__main__':
    controller=QuoteGUIController()
    controller.run()
