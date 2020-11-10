# -*- coding: utf-8 -*-

import sys
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 and minor==6 :
    import tkinter as tk
    from tkinter import filedialog
else :
    import tkinter as tk
    from tkinter import filedialog 

from math import pi,sin
import collections
import subprocess
import sqlite3

from observer import *
from piano import *
import wave_generator  as generator
import wave_visualizer as visualizer
import keyboard 

mw = tk.Tk()
mw.geometry("1280x720")
mw.title("Leçon de Piano")

menubar=generator.Menubar(mw)

class Piano():
    def __init__(self, parent):
        self.frame = tk.Frame(parent, borderwidth=5)
        self.model = keyboard.Octave(4)
        self.view = keyboard.Screen(self.frame)
        self.model.attach(self.view)
        self.control = keyboard.Keyboard(self.frame, self.model)

        # keyboard packing
        self.view.get_screen().pack()
        self.control.get_keyboard().pack()
        pass

class Visualizer():
    def __init__(self, parent):
        self.frame = frame_signal=tk.Frame(parent, borderwidth=5)

        self.view = visualizer.Screen(self.frame)
        self.view.grid(10)
        self.view.packing()

        self.model = visualizer.Visualizer()
        self.model.attach(self.view)
        self.model.generate_signal()
        pass

class Generator():
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.view = generator.Interface(self.frame)
        self.view.packing()
        self.model = generator.Generator()
        self.model.attach(self.view)
        pass

class Controller:
    def __init__(self, generator, piano, visualizer):
        self.generator = generator
        self.piano = piano
        self.visualizer = visualizer

        self.notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        pass

    def on_note_generate(self):
        pass


gene = Generator(mw)
piano = Piano(mw)
visu = Visualizer(mw)

gene.frame.grid(column=0, row=0)
visu.frame.grid(column=1, row=0)
piano.frame.grid(column=0, columnspan=2, row=1)

controller = Controller(gene, piano, visu)

mw.mainloop()