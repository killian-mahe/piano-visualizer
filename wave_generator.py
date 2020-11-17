# -*- coding: utf-8 -*-

import sys
print("Your platform is : " ,sys.platform)
major=sys.version_info.major
minor=sys.version_info.minor
print("Your python version is : ",major,minor)
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 and minor==6 :
    import tkinter as tk
    from tkinter import filedialog
else :
    print("with this version ... I guess it will work ! ")
    import tkinter as tk
    from tkinter import filedialog 

import shutil
import copy
from Utils.listes import ListMenu
from observer import Observer, Subject
from Utils.path_to_files import is_file
from Audio import audio_wav
import sqlite3
import subprocess

class Interface(Observer):
    def __init__(self, parent, width=600, height=600, from_=1, to=10):
        Observer.__init__(self)
        self.frame = tk.LabelFrame(parent, text="Generator ", borderwidth=5, padx=20, pady=20)
        # self.menu = Menubar(parent)
        self.notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        self.octave = tk.IntVar()
        self.octave.set(4)

        # Note selection
        self.noteList = tk.Listbox(self.frame, height=15, bd=4, selectborderwidth=1)
        for note in self.notes:
            self.noteList.insert("end", note)

        # Octave selection
        self.octaveScale = tk.Scale(self.frame, variable=self.octave, label="Octave", orient="vertical", length=350, from_=from_, to=to, tickinterval=1)

        # Generate Button
        self.generateButton = tk.Button(self.frame, text="Generate")

        # Play Button
        self.playButton = tk.Button(self.frame, text="Play note", bg="light sky blue")
        self.playChordButton = tk.Button(self.frame, text="Play chord", bg="light sky blue")

        # Chords prepate
        self.addToChord = tk.Button(self.frame, text="Add to chord => ")
        self.chordPrepareListbox = tk.Listbox(self.frame, height=5, bd=4, selectborderwidth=1)

        # Generate chord
        self.generateChord = tk.Button(self.frame, text="Generate chord")

        # Chords selection
        self.chordsSelection = tk.Listbox(self.frame, height=15, bd=4, selectborderwidth=1)

    def update(self, model):
        self.notes = model.notes
        self.noteList.delete(0, 'end')
        self.chordsSelection.delete(0, 'end')
        self.chordPrepareListbox.delete(0, 'end')

        for note in self.notes:
            self.noteList.insert("end", note)

        for chord in model.chordsList:
            self.chordsSelection.insert("end", ", ".join(chord))
    
        for note in model.chordInPrepare:
            self.chordPrepareListbox.insert("end", note)
        
        pass
    
    def packing(self):
        self.frame.pack()
        self.generateButton.grid(column=0, row=1)
        self.octaveScale.grid(column=0, row=0)

        self.noteList.grid(column=1, row=0)
        self.playButton.grid(column=1, row=1)
        
        self.addToChord.grid(column=2, row=0)

        self.chordPrepareListbox.grid(column=3, row=0)
        self.generateChord.grid(column=3, row=1)

        self.chordsSelection.grid(column=4, row=0)
        self.playChordButton.grid(column=4, row=1)
        return

class Generator(Subject):
    def __init__(self):
        Subject.__init__(self)
        self.__notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        self.chordInPrepare = []
        self.chordsList = [["C4", "E4", "G4"]]
        pass
    
    @property
    def notes(self):
        return self.__notes
    
    @notes.setter
    def notes(self, notes):
        self.__notes = notes
        self.notify()
        pass

    def play_notes(self, notes, octave=4):
        if type(notes) is list:
            self.generateChord(notes)
            chord = "".join(notes)
            subprocess.call(["aplay", "Chords/"+chord+".wav"])
        else:
            self.generateNote(notes, octave)
            subprocess.call(["aplay", "Sounds/"+notes+str(octave)+".wav"])
        pass

    def add_note_to_chord(self, note, degree):
        self.chordInPrepare.append(note+str(degree))
        self.notify()
        pass

    def create_chord(self):
        if len(self.chordInPrepare) > 1:
            self.generateChord(copy.copy(self.chordInPrepare))
            self.chordsList.append(copy.copy(self.chordInPrepare))
            self.chordInPrepare.clear()
            self.notify()
        pass

    def get_frequency(self, note, octave = 4):
        connect = sqlite3.connect("Audio/frequencies.db")
        cursor = connect.cursor()
        result = cursor.execute("SELECT \"{}\" FROM frequencies WHERE octave={};".format(note.replace('#', "Sharp"), octave))
        connect.commit()
        result = result.fetchone()[0]
        connect.close()

        return result

    def generateNote(self, note, octave=4):
        file_name = str(note)+str(octave)+'.wav'
        folder = 'Sounds'

        if not is_file(folder, file_name) :
            freq = self.get_frequency(note, octave)
            audio_wav.save_note_wav(folder+'/'+file_name, freq, 2*freq)
        
        pass

    def generateChord(self, notes):
        chord_name = "".join(notes)+".wav"
        sound_folder = 'Sounds'
        chord_folder = 'Chords'
        chords = []
        data = []

        if is_file(chord_folder, chord_name):
            print('Already generated !')
            return

        for note in notes:
            self.generateNote(note[0:-1], note[-1::])
            file_name = str(note)+'.wav'
            chords.append(audio_wav.open_wav(sound_folder+ '/' +file_name))

        for i in range(len(chords[0][0])):
            sum = 0
            for j in range(len(chords)):
                sum += chords[j][0][i]
            data.append(sum/len(chords))

        audio_wav.save_wav(chord_name,data,chords[0][1])
        shutil.move(chord_name, chord_folder+'/'+chord_name)
        pass

class Controller:
    def __init__(self, parent, model : Generator, view : Interface):
        self.model = model
        self.view = view
        self.view.generateButton.bind("<Button-1>", self.on_note_generate)
        self.view.addToChord.bind("<Button-1>", self.composeChord)
        self.view.generateChord.bind("<Button-1>", self.generateChord)
        self.view.playChordButton.bind("<Button-1>", self.playChord)
        self.view.playButton.bind("<Button-1>", self.playNote)
        pass
    
    def on_note_generate(self, event):
        self.model.generateNote(self.view.noteList.get('active'), self.view.octave.get())
        pass

    def composeChord(self, event):
        self.model.add_note_to_chord(self.view.noteList.get('active'), self.view.octave.get())
        pass

    def generateChord(self, event):
        self.model.create_chord()
        pass

    def playChord(self, event):
        self.model.play_notes(self.view.chordsSelection.get('active').split(', '))
        pass

    def playNote(self, event):
        note = self.view.noteList.get('active')
        degree = self.view.octaveScale.get()
        self.model.play_notes(note, degree)
        pass


class Menubar(tk.Frame):
    def __init__(self,parent=None):
        tk.Frame.__init__(self, borderwidth=2)
        if parent :
            menu = tk.Menu(parent)
            parent.config(menu=menu)
            fileMenu = tk.Menu(menu)
            fileMenu.add_command(label="Save",command=self.save)
            menu.add_cascade(label="File", menu=fileMenu)
        pass

    def save(self):
        formats=[('Texte','*.py'),('Portable Network Graphics','*.png')]
        filename=filedialog.asksaveasfilename(parent=self,filetypes=formats,title="Save...")
        if len(filename) > 0:
            print("Sauvegarde en cours dans %s" % filename)
        pass

if __name__ == "__main__" :
    mw=tk.Tk()

    mw.geometry("900x900")
    mw.title("Generateur de fichier au format WAV")

    model = Generator()
    view = Interface(mw)
    view.packing()
    model.attach(view)

    ctrl = Controller(mw, model, view)

    mw.mainloop()
