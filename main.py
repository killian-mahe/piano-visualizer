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
import time

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
    def __init__(self, generator : Generator, piano : Piano, visualizer : Visualizer):
        self.generator = generator
        self.piano = piano
        self.visualizer = visualizer

        self.piano.control.on_click= self.on_keyboard_click
        self.generator.view.generateButton.bind("<Button-1>", self.on_note_generate)
        self.generator.view.playButton.bind("<Button-1>", self.on_note_play)
        self.generator.view.playChordButton.bind("<Button-1>", self.on_chord_play)
        pass

    def on_note_generate(self, event):
        note = self.generator.view.noteList.get('active')
        self.generator.model.generateNote(self.generator.view.noteList.get('active'), self.generator.view.octave.get())
        freq = self.generator.model.get_frequency(note, 4)
        self.visualizer.model.set_frequency(freq)
        self.visualizer.model.generate_signal()
        pass
    
    def on_keyboard_click(self, key):
        if type(key) is list:
            return
        freq = self.generator.model.get_frequency(key, 4)
        self.visualizer.model.set_frequency(freq)
        self.visualizer.model.generate_signal()
        pass

    def on_note_play(self, event):
        note = self.generator.view.noteList.get('active')
        self.piano.control.reset_note()
        self.piano.control.show_note([note])
        self.piano.control.play_note(note)
        pass

    def on_chord_play(self, event):
        chord = self.generator.view.chordsSelection.get("active")
        self.generator.model.generateChord(chord.split(', '))
        self.piano.control.reset_note()
        self.piano.control.show_note(chord.split(', '))
        self.piano.control.play_note(chord.split(', '))
        pass


gene = Generator(mw)
piano = Piano(mw)
visu = Visualizer(mw)

gene.frame.grid(column=0, row=0)
visu.frame.grid(column=1, row=0)
piano.frame.grid(column=0, columnspan=2, row=1)

controller = Controller(gene, piano, visu)

mw.mainloop()