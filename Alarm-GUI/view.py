#!/usr/bin/python3

import tkinter as tk
import tkinter.ttk as ttk
import random
from tkinter import messagebox


class GUIView:
    def __init__(self, alarm_state):
        self.alarm_state = alarm_state
        self.window = tk.Tk()
        self.window.title("HouseGuard")

        self.wait = False

        style = ttk.Style()
        font = ('calibri', 86, 'bold')
        style.configure('TLabel', font=font, borderwidth='4')

        style.map('TLabel', foreground=[('!active', 'blue')])
        style.configure('TButton', font=font, borderwidth='4')

        style.map('TButton', foreground=[('active', '!disabled', 'white')],
                  background=[('active', 'purple')])

        frame3 = tk.Frame(self.window)
        frame3.pack()
        text = "{}".format(self.alarm_state)
        self.state_label = ttk.Label(frame3, text=text)
        self.state_label.pack()

        frame4 = tk.Frame(self.window)
        frame4.pack()
        self.on_button = ttk.Button(frame4, text="ON", command=self.on_event)
        self.off_button = ttk.Button(
            frame4, text="OFF", command=self.off_event)

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
        if not self.wait:
            self.state_label['text'] = 'ON'

    def off_event(self):
        if not self.wait:
            self.state_label['text'] = 'OFF'

    def show_wait(self):
        self.wait = True
        messagebox.showwarning('Warning', 'Please wait')
