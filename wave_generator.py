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

from Utils.listes import *
from observer import Observer, Subject

class Interface(Observer):
    def __init__(self, parent, width=600, height=600):
        Observer.__init__(self)
    
    def packing(self):
        return

class Generator(Subject):
    def __init__(self):
        Subject.__init__(self)

class Controller:
    def __init__(self, parent, model, view):
        self.model = model
        self.view = view
        self.notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        self.create_controls(parent)

    def create_controls(self, parent):
        self.menu = Menubar(parent)
        self.frame = tk.LabelFrame(mw, text="Generator ", borderwidth=5, width=400, height=300, bg="pink")

    def packing(self):
        self.frame.pack()


class Menubar(tk.Frame):
    def __init__(self,parent=None):
        tk.Frame.__init__(self, borderwidth=2)
        if parent :
            menu = tk.Menu(parent)
            parent.config(menu=menu)
            fileMenu = tk.Menu(menu)
            fileMenu.add_command(label="Save",command=self.save)
            menu.add_cascade(label="File", menu=fileMenu)

    def save(self):
        formats=[('Texte','*.py'),('Portable Network Graphics','*.png')]
        filename=filedialog.asksaveasfilename(parent=self,filetypes=formats,title="Save...")
        if len(filename) > 0:
            print("Sauvegarde en cours dans %s" % filename)

if __name__ == "__main__" :
    mw=tk.Tk()
    mw.geometry("360x300")
    mw.title("Generateur de fichier au format WAV")

    model = Generator()
    view = Interface(mw)
    view.packing()

    ctrl = Controller(mw, model, view)
    ctrl.packing()

    mw.mainloop()
