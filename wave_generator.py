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

from Utils.listes import ListMenu
from observer import Observer, Subject
import subprocess

class Interface(Observer):
    def __init__(self, parent, width=600, height=600):
        Observer.__init__(self)
        self.frame = tk.LabelFrame(parent, text="Generator ", borderwidth=5, width=400, height=300)
        self.menu = Menubar(parent)
        self.notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

        # Note selection
        self.noteList = tk.Listbox(self.frame)
        for note in self.notes:
            self.noteList.insert("end", note)

        # Generate Button
        self.generateButton = tk.Button(self.frame, text="Generate")
        pass

    def update(self, model):
        self.notes = model.notes
        self.noteList.delete(0)
        for note in self.notes:
            self.noteList.insert(note)
        pass
    
    def packing(self):
        self.frame.pack()
        self.noteList.pack()
        self.generateButton.pack()
        return

class Generator(Subject):
    def __init__(self):
        Subject.__init__(self)
        self.__notes = []
        pass
    
    @property
    def notes(self):
        return self.__notes
    
    @notes.setter
    def notes(self, notes):
        self.notes = notes
        self.notify()
        pass

class Controller:
    def __init__(self, parent, model : Generator, view : Interface):
        self.model = model
        self.view = view
        self.view.generateButton.bind("<Button-1>", self.on_note_generate)
        pass
    
    def on_note_generate(self, event):
        note = self.view.noteList.get('active')
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

    mw.geometry("360x300")
    mw.title("Generateur de fichier au format WAV")

    model = Generator()
    view = Interface(mw)
    view.packing()
    model.attach(view)

    ctrl = Controller(mw, model, view)

    mw.mainloop()
