#!/usr/bin/python3

import model
import view


class GUIController:
    def __init__(self):
        self.view = view.GUIView('ON')
        self.model = model.Model()

    def run(self):
        self.view.on_button.bind("<Button-1>", self.btnClicked)
        self.view.window.mainloop()

    def btnClicked(self, event):
        value = 0
