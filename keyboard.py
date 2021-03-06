# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter

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
    print("with your python version : ",major,minor)
    print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 

from math import pi,sin
import collections
import subprocess
from observer import *


class Octave(Subject) :
    """ Octave Model """
    def __init__(self,degree=3) :
        Subject.__init__(self)
        self.sound_folder = 'Sounds'
        self.chord_folder = 'Chords'
        self.degree=degree
        self.set_sounds_to_gamme(degree)
    def get_gamme(self) :
        return self.gamme
    def set_gamme(self,gamme) :
        self.gamme=gamme
    def get_degree(self) :
        return self.degree
    def notify(self,key) :
        for obs in self.observers:
            obs.update(self,key)

    def set_sounds_to_gamme(self,degree=3) :
        self.degree=degree
        folder="Sounds"
        notes=["C","D","E","F","G","A","B","C#","D#","F#","G#","A#"]
        self.gamme=collections.OrderedDict()
        for key in notes :
            self.gamme[key]=self.sound_folder+"/"+key+str(degree)+".wav"
        return self.gamme

class Screen(Observer):
    """ Octave View """
    def __init__(self,parent) :
        self.parent=parent
        self.screen=tk.Frame(self.parent,borderwidth=5,width=500,height=160,bg="pink")
        self.info=tk.Label(self.screen,text="Appuyez sur une touche clavier ",bg="pink",font=('Arial',10))
        self.packing()

    def get_screen(self) :
        return self.screen

    def update(self,model,key="C") :
        """Octave View update"""
        if type(key) is list:
            chord = "".join(key)
            subprocess.call(["aplay", model.chord_folder+"/"+chord+".wav"])
            return
        subprocess.call(["aplay",model.get_gamme()[key]])
        if self.info :
            self.info.config(text="Vous avez joue la note: "+ key + str(model.get_degree()))
            
    def packing(self):
        self.info.pack()
        pass
    

class Keyboard :
    """ Octave controller """
    def __init__(self,parent,model, on_click=False) :
        self.parent=parent
        self.model=model
        self.buttons = {}
        self.on_click = on_click
        self.create_keyboard()
    def create_keyboard(self, key_w=40,key_h=150) :
        
        dx_white,dx_black=0,0
        self.keyboard=tk.Frame(self.parent,borderwidth=3, width=7.2*key_w,height=1.05*key_h,bg="red")
        for key in self.model.gamme.keys() :
            if key.startswith('#',1,len(key)) :
                delta_w,delta_h=3/4.,2/3.
                delta_x=3/5.
                button=tk.Button(self.keyboard,text=key, anchor="s",name=key.lower(), fg="white",width=3,height=6,bg="black")
                button.bind("<Button-1>",lambda event,x=key : self.play_note(x))
                button.place(width=key_w*delta_w,height=key_h*delta_h,x=key_w*delta_x+key_w*dx_black,y=0)
                if key.startswith('D#',0,len(key) ) :
                    dx_black=dx_black+2
                else :
                    dx_black=dx_black+1
            else :
                button=tk.Button(self.keyboard,text=key, anchor="s",name=key.lower(),bg = "white")
                button.bind("<Button-1>",lambda event,x=key : self.play_note(x))
                button.place(width=key_w,height=key_h,x=key_w*dx_white,y=0)
                dx_white=dx_white+1
            self.buttons[key] = button

    def play_note(self,key) :
        """Octave Controller Action"""
        self.model.notify(key)
        if (self.on_click) :
            self.on_click(key, self.model.degree)
    
    def show_note(self, keys):
        for key in keys:
            button = self.buttons.get(key)
            button.configure(bg = 'sky blue')
        pass

    def reset_note(self):
        for key, val in self.buttons.items():
            if key.startswith('#',1,len(key)):
                val.configure(bg = 'black')
            else:
                val.configure(bg = 'white')

    def get_keyboard(self) :
        return self.keyboard
    def get_degrees(self) :
        return self.degrees

if __name__ == "__main__" :
    mw = tk.Tk()
    mw.geometry("360x300")
    degree=3
    mw.title("Clavier pour octave de degré " + str(degree))
    model=Octave(degree)
    control=Keyboard(mw,model)
    view=Screen(mw)
    model.attach(view)
    control.get_keyboard().grid(column=degree,row=0)
    view.get_screen().grid(column=degree,row=1)
    mw.mainloop()
