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
from Utils.listes import ListMenu
from observer import Observer, Subject
from Utils.path_to_files import is_file
from Audio import audio_wav
import sqlite3
import subprocess

class Interface(Observer):
    def __init__(self, parent, width=600, height=600):
        Observer.__init__(self)
        self.frame = tk.LabelFrame(parent, text="Generator ", borderwidth=5, padx=20, pady=20)
        self.menu = Menubar(parent)
        self.notes = []
        self.generatedNotes = []
        self.octave = tk.IntVar()
        self.octave.set(4)

        # Note selection
        self.noteList = tk.Listbox(self.frame, height=15, bd=4, selectborderwidth=1)
        for note in self.notes:
            self.noteList.insert("end", note)

        # Octave selection
        self.octaveScale = tk.Scale(self.frame, variable=self.octave, label="Octave", orient="vertical", length=350, from_=-1, to=10, tickinterval=1)

        # Generate Button
        self.generateButton = tk.Button(self.frame, text="Generate")

        # Generated notes
        self.arrowLabel = tk.Label(self.frame, text="=>", padx=20)
        self.generatedNoteList = tk.Listbox(self.frame, height=15, bd=4, selectborderwidth=1)
        pass

    def update(self, model):
        self.notes = model.notes
        self.noteList.delete(0)
        for note in self.notes:
            self.noteList.insert("end", note)
        pass
    
    def packing(self):
        self.frame.pack()
        self.noteList.grid(column=1, row=0)
        self.generateButton.grid(column=0, columnspan=2, row=1)
        self.octaveScale.grid(column=0, row=0)
        self.arrowLabel.grid(column=2, row=0)
        self.generatedNoteList.grid(column=3, row=0)
        return

class Generator(Subject):
    def __init__(self):
        Subject.__init__(self)
        self.__notes = []
        self.__generatedNotes = []
        pass
    
    @property
    def notes(self):
        return self.__notes
    
    @notes.setter
    def notes(self, notes):
        self.__notes = notes
        self.notify()
        pass

    @property
    def generatedNotes(self):
        return self.__generatedNotes;

    @generatedNotes.setter
    def generatedNotes(self, notes):
        self.__generatedNotes = notes;
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
        
        subprocess.call(["aplay", 'Sounds/'+file_name])

        pass

class Controller:
    def __init__(self, parent, model : Generator, view : Interface):
        self.model = model
        self.model.notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        self.view = view
        self.view.generateButton.bind("<Button-1>", self.on_note_generate)
        pass
    
    def on_note_generate(self, event):
        note = self.view.noteList.get('active')
        self.model.generateNote(self.view.noteList.get('active'), self.view.octave.get())
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
