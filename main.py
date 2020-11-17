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
import piano as p
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
        self.octaves = []
        piano = p.Piano(self.frame, 4)
        self.octaves = piano.octaves
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
        self.view = generator.Interface(self.frame, from_=2, to=5)
        self.view.packing()
        self.model = generator.Generator()
        self.model.attach(self.view)
        self.control = generator.Controller(self.frame, self.model, self.view)
        pass

class Controller:
    def __init__(self, generator : Generator, piano : Piano, visualizer : Visualizer):
        self.generator = generator
        self.piano = piano
        self.visualizer = visualizer

        for octave in self.piano.octaves:
            octave.on_click = self.on_keyboard_click
        self.generator.view.generateButton.bind("<Button-1>", self.on_note_generate)
        self.generator.view.playButton.bind("<Button-1>", self.on_note_play)
        self.generator.view.playChordButton.bind("<Button-1>", self.on_chord_play)
        pass

    def on_note_generate(self, event):
        note = self.generator.view.noteList.get('active')
        degree = self.generator.view.octaveScale.get()
        freq = self.generator.model.get_frequency(note, degree)
        self.generator.model.generateNote(note, degree)
        self.visualizer.model.set_frequency(freq)
        self.visualizer.model.generate_signal()
        pass
    
    def on_keyboard_click(self, key, degree):
        if type(key) is list:
            return
        self.visualizer.model.set_frequency(self.generator.model.get_frequency(key, degree))
        self.visualizer.model.generate_signal()
        pass

    def on_note_play(self, event):
        note = self.generator.view.noteList.get('active')
        degree = self.generator.view.octaveScale.get()
        if 1 < degree < 5:
            self.piano.octaves[degree-2].play_note(note)
        pass

    def on_chord_play(self, event):
        chord = self.generator.view.chordsSelection.get('active').split(', ')
        self.generator.model.play_notes(chord)

        for octave in self.piano.octaves:
            octave.reset_note()

        for note in chord:
            degree = note[-1::]
            self.piano.octaves[int(degree)-2].show_note(note[0:-1])
        pass


gene = Generator(mw)
piano = Piano(mw)
visu = Visualizer(mw)

gene.frame.grid(column=0, row=0)
visu.frame.grid(column=1, row=0)
piano.frame.grid(column=0, columnspan=2, row=1)

controller = Controller(gene, piano, visu)

mw.mainloop()