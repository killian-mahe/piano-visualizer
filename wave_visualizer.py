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

from math import pi,sin,cos
from observer import Observer, Subject

class Visualizer(Subject):
    def __init__(self):
        Subject.__init__(self)
        self.signal = []
        self.a, self.f, self.p, self.h = 1.0, 1.0, 0.0, 1

    def get_signal(self) :
        return self.signal

    def set_magnitude(self, a) :
        self.a = a

    def set_frequency(self, f) :
        self.f = f

    def set_harmonic(self, h):
        self.h = h
    
    def set_phase(self, p):
        self.p = p
    
    def generate_signal(self, period=2, samples=100.0):
        del self.signal[0:]
        echantillons=range(int(samples) + 1)
        Tech = period / samples
        for t in echantillons :
            self.signal.append([t*Tech, self.vibration(t*Tech, self.h)])
        self.notify()
        return self.signal
    
    def vibration(self, t, harmoniques=1, impair=True):
        a, f, p = self.a, self.f, self.p
        somme = 0
        for h in range(1, harmoniques + 1) :
            somme = somme + (a*1.0/h) * sin(2*pi * (f*h)*t - p)
        return somme

class Screen(Observer):
    def __init__(self, parent, bg="white", width=600, height=300):
        Observer.__init__(self)
        self.canvas = tk.Canvas(parent, bg=bg, width=width, height=height)
        self.a, self.f, self.p = 10.0, 2.0, 0.0
        self.signal = []
        self.width, self.height = width, height
        self.units = 1
        self.canvas.bind("<Configure>", self.resize)

    def update(self, model):
        self.signal = model.get_signal()
        self.canvas.delete("sound")
        self.plot_signal(self.signal)

    def plot_signal(self, signal, color="red"):
        w, h = self.width, self.height
        signal_id = None

        if signal and len(signal) > 1:
            plot = [(x*w,h/2.0*(1-y*1.0/(self.units/2.0))) for (x, y) in signal]
            signal_id = self.canvas.create_line(plot, fill=color, smooth=1, width=3,tags="sound")

        return signal_id

    def grid(self, steps=2):
        self.units = steps
        tile_x = self.width / steps

        for t in range(1, steps+1):
            x = t * tile_x
            self.canvas.create_line(x, 0, x, self.height, tags="grid")
            self.canvas.create_line(x, self.height/2 - 10, x, self.height/2 + 10, width=3, tags="grid")
        
        tile_y=self.height/steps
        
        for t in range(1,steps+1):
            y = t * tile_y
            self.canvas.create_line(0, y, self.width, y, tags="grid")
            self.canvas.create_line(self.width/2 - 10, y, self.width/2 + 10, y, width=3, tags="grid")

    def resize(self,event):
        if event:
            self.width, self.height=event.width, event.height
            self.canvas.delete("grid")
            self.canvas.delete("sound")
            self.grid(self.units)
            self.plot_signal(self.signal)

    def packing(self) :
        self.canvas.pack(expand=1, fill="both", padx=6)
    
class Controller : 
    def __init__(self, parent, model, view):
        self.model = model
        self.view = view
        self.create_controls(parent)

    def create_controls(self, parent):
        self.frame = tk.LabelFrame(parent, text="Paramètres", borderwidth=5, width=600, height=300)
        
        self.amp = tk.IntVar()
        self.amp.set(1)
        self.scaleA = tk.Scale(self.frame, variable=self.amp,
                                label="Amplitude", orient="horizontal",
                                length=550, from_=0, to=5, tickinterval=1)
        self.scaleA.bind("<B1-Motion>", self.update_magnitude)

        self.freq = tk.IntVar()
        self.freq.set(1)
        self.scaleF = tk.Scale(self.frame, variable=self.freq,
                                label="Fréquence", orient="horizontal",
                                length=550, from_=0, to=10,
                                resolution=1, tickinterval=1)
        self.scaleF.bind("<B1-Motion>", self.update_frequency)

        self.harm = tk.IntVar()
        self.harm.set(1)
        self.scaleH = tk.Scale(self.frame, variable=self.harm,
                                label="Harmoniques", orient="horizontal",
                                length=550, from_=0, to=5,
                                resolution=1, tickinterval=1)
        self.scaleH.bind("<B1-Motion>", self.update_harmonic)

        self.phase = tk.IntVar()
        self.phase.set(1)
        self.scaleP = tk.Scale(self.frame, variable=self.phase,
                                label="Phase", orient="horizontal",
                                length=550, from_=0, to=90,
                                resolution=1, tickinterval=10)
        self.scaleP.bind("<B1-Motion>", self.update_phase)

    def update_magnitude(self, event):
        self.model.set_magnitude(self.amp.get())
        self.model.generate_signal()

    def update_frequency(self, event):
        self.model.set_frequency(self.freq.get())
        self.model.generate_signal()

    def update_harmonic(self, event):
        self.model.set_harmonic(self.harm.get())
        self.model.generate_signal()

    def update_phase(self, event):
        self.model.set_phase(self.phase.get())
        self.model.generate_signal()

    def packing(self):
        self.frame.pack()
        self.scaleA.pack()
        self.scaleF.pack()
        self.scaleH.pack()
        self.scaleP.pack()

if __name__ == "__main__" :
    mw = tk.Tk()
    mw.geometry("600x700")
    mw.title("Visualisation de signal sonore")
    
    model = Visualizer()
    view = Screen(mw)
    view.grid(8)
    view.packing()
    
    model.attach(view)
    model.generate_signal()
    ctrl = Controller(mw, model, view)
    ctrl.packing()
    
    mw.mainloop()
