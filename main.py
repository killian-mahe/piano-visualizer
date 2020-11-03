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
    print("with your python version : ",major,minor)
    print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 

from math import pi,sin
import collections
import subprocess
from observer import *
from piano import *
from wave_visualizer import *
from wave_generator import *


mw = tk.Tk()
mw.geometry("360x300")
mw.title("Leçon de Piano")
frame=tk.Frame(mw,borderwidth=5,width=360,height=300)
octaves=2
piano=Piano(frame,octaves)
view=View(frame)
view.grid(4)
view.packing()
view.update()
frame.pack()    
mw.mainloop()
