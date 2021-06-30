#!/usr/bin/python3

# import required modules
import tkinter as tk
import sys
import queue
import threading
from enum import Enum

class Messages(Enum):
    WRITEMSG = 1
    
def workcycle(guiref, model, q):
    msg = None
    while True:
        try:
            msg = q.get(timeout=0.1)
            
            if hasattr(msg, 'type'):
                if msg.type == Messages.WRITEMSG:
                    bytes = bytearray(msg.entry.get().encode("ASCII"))
                    print('Hi')
                    
        except queue.Empty:
            pass
          
        read = model.port.read(model.port.in_waiting)
        if len(read) > 0:
            guiref.label.set(read.decode())
            
def gui(root, q):
    labelVal = tk.StringVar()
    entryVal = tk.StringVar()
    e = tk.Entry(root, textvariable=entryVal)
    l = tk.Label(root, textvariable=labelVal)
    cb = lambda : q.put(SimpleNamespace(type=Messages.WRITEMSG, label=labelVal, entry=e))
    b = tk.Button(root, text="Send message", command=cb)
    e.pack()
    b.pack()
    l.pack()
    return SimpleNamespace(label=labelVal)

# class Application:

# 	def __init__(self):
# 		'''Constructor'''
# 		self.alarm_state = 'N/A'
# 		self.tk = Tk()
# 		self.frame = Frame(self.tk)
# 		self.tk.title("Weather App")
# 		# adjust window size
# 		self.state = False
# 		self.tk.bind("<F11>", self.toggle_fullscreen)
# 		self.tk.bind("<Escape>", self.end_fullscreen)
# 		self.text = StringVar()
# 		self.state_label = ''
# 		self.toggle_fullscreen()

# 	def toggle_fullscreen(self, event=None):
# 		self.state = not self.state  # Just toggling the boolean
# 		self.tk.attributes("-fullscreen", self.state)
# 		return "break"

# 	def end_fullscreen(self, event=None):
# 		self.state = False
# 		self.tk.attributes("-fullscreen", self.state)
# 		return "break"

# 	def set_buttons(self):
# 		on_button = Button(self.tk, text="ON",
# 							width=12, command=self.on_event)
# 		on_button.pack()
# 		off_button = Button(self.tk, text="OFF",
# 							width=12, command=self.off_event)
# 		off_button.pack()
	
# 	def set_labels(self):
# 		text = "Alarm State: {}".format(self.alarm_state)
# 		self.state_label = Label(self.tk, text=text)
# 		self.state_label.pack()

# 	def on_event(self):
# 		print('On Button Clicked')
# 		self.state_label['text'] = 'Alarm State: ON'

# 	def off_event(self):
# 		print('Off Button Clicked')
# 		self.state_label['text'] = 'Alarm State: OFF'

# 	def setup(self):
# 		# add labels, buttons and text
# 		self.set_labels()
# 		self.set_buttons()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		exit(1)
	port = serial.Serial(port=sys.argv[1], baudrate=115200, timeout=0.1)
	q = queue.Queue()
	root = tk.Tk()
	guiref = gui(root, q)
	model = SimpleNamespace(port=port)
	t = threading.Thread(target=workcycle, args=(guiref, model,q))
	t.daemon = True
	t.start()
	'''app = Application()
	app.setup()
	app.tk.mainloop()'''