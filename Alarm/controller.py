#!/usr/bin/python3

import model
import view
import threading
import time
import logging


class GUIController:
    def __init__(self, name):
        self.view = view.GUIView('ON')
        self.model = model.Model(name)
        self.model.get_settings()

    def run(self):
        self.view.on_button.bind("<Button>", self.onClicked)
        self.view.off_button.bind("<Button>", self.offClicked)
        self.view.window.bind("<<event1>>",
                              self.eventhandler)
        thd = threading.Thread(target=self.timecnt)
        # timer thread
        thd.daemon = True
        thd.start()
        self.view.window.mainloop()

    def onClicked(self, event):
        self.model.set_data('ON')
        self.view.state_label['text'] = 'ON'

    def offClicked(self, event):
        self.model.set_data('OFF')
        self.view.state_label['text'] = 'OFF'

    def timecnt(self):
        # runs in background thread
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
        # event thread id (same as main)
        self.model.publish_data()
        # 123, data from event
