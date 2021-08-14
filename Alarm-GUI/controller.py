#!/usr/bin/python3

import model
import view


class GUIController:
    def __init__(self):
        self.view = view.GUIView('ON')
        self.model = model.Model()

    def run(self):
        self.view.on_button.bind("<Button>", self.onClicked)
        self.view.off_button.bind("<Button>", self.offClicked)
        self.view.window.mainloop()

    def onClicked(self, event):
        if not self.model.check_time():
            self.view.show_wait()
        else:
            if self.model.publish_data('ON'):
                self.view.state_label['text'] = 'ON'

    def offClicked(self, event):
        if not self.model.check_time():
            self.view.show_wait()
        else:
            if self.model.publish_data('OFF'):
                self.view.state_label['text'] = 'OFF'
