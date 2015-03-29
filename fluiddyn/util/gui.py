"""Graphical user interface (:mod:`fluiddyn.util.gui`)
======================================================




"""

import sys

try: # Python 3
    import tkinter as tk
    from tkinter import N, W, E, S, END
    from tkinter import ttk
    from tkinter.scrolledtext import ScrolledText
    from tkinter.simpledialog import SimpleDialog
    import tkinter.font as font
except ImportError: # Python 2
    import Tkinter as tk
    from Tkinter import N, W, E, S, END
    import ttk
    from ScrolledText import ScrolledText
    from tkSimpleDialog import Dialog as SimpleDialog
    import tkFont as font

import time
import datetime as dt


from fluiddyn._version import __version__
from fluiddyn.util.deamons import DaemonThread as Daemon



from fluiddyn.lab.rotatingobjects import (
    create_rotating_objects_kepler,
    DaemonRunningRotatingObject, 
    RotatingObject)







class ElapsedTimeClock(ttk.Label):
    def __init__(self, parent, *args, **kwargs):
        ttk.Label.__init__(self, parent, *args, **kwargs)
        self.lasttime = ""
        t = time.localtime()
        self.zerotime = dt.timedelta(hours=t[3], minutes=t[4], seconds=t[5])
        self.tick()

    def tick(self):
        # get the current local time from the PC
        now = dt.datetime(1, 1, 1).now()
        elapsedtime = now - self.zerotime
        time2 = elapsedtime.strftime('%H:%M:%S')
        # if time string has changed, update it
        if time2 != self.lasttime:
            self.lasttime = time2
            self.config(text=time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
        self.after(200, self.tick)















class FrameRotatingObject(ttk.Frame):
    """A simple frame for an object with a write function."""
    def __init__(self, master, obj, title=None, **kargs):
        self.obj = obj
        if title is None:
            self.title = obj.name

        ttk.Frame.__init__(self, master)
        self.create_widgets()
        self.grid(sticky=(N, W, E, S), **kargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


    def create_widgets(self):

        label_title = ttk.Label(self, text=self.title, font='TkHeadingFont')
        label_title.grid(column=0, row=0, padx=15)

        label = ttk.Label(self, text='rotation rate:',
                          font='TkHeadingFont')
        label.grid(column=0, row=1, padx=15)

        self.stringvar_rr = tk.StringVar()
        self.stringvar_rr.set('{:5.2f}'.format(self.obj.rotation_rate))
        self.label_rr = ttk.Label(
            self, textvariable=self.stringvar_rr,
            font='TkHeadingFont')
        self.label_rr.grid(column=1, row=1, padx=15)

        label = ttk.Label(self, text='rad/s',
                          font='TkHeadingFont')
        label.grid(column=2, row=1, padx=15)

        self._redefine_write()


    def _redefine_write(self):
        """Dynamically overwrite the function write of the object."""

        def new_write(obj, string):
            # print(string)
            self.stringvar_rr.set('{:7.3f}'.format(self.obj.rotation_rate))

        # To dynamically overwrite an instance method:
        instancemethod = type(self.obj.write)
        # info on instancemethod:
        # Type:       type
        # String Form:<type 'instancemethod'>
        # Docstring:
        #     instancemethod(function, instance, class)
        #     Create an instance method object.
        self.obj.write = instancemethod(
            new_write, self.obj, self.obj.__class__)










class FrameWritingObject(ttk.Frame):
    """A simple frame for an object with a write function."""
    def __init__(self, master, obj, title=None, **kargs):
        self.obj = obj
        if title is None:
            self.title = obj.name

        ttk.Frame.__init__(self, master)
        self.create_widgets()
        self.grid(sticky=(N, W, E, S), **kargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


    def create_widgets(self):

        label_title = ttk.Label(self, text=self.title, font='TkHeadingFont')
        label_title.grid(column=0, row=0, padx=15)

        self.text = ScrolledText(self, height=6)
        self.text.grid(
            column=0, row=1, padx=10, pady=10,
            sticky=(N, W, E, S))

        self._redefine_write()


    def _redefine_write(self):
        """Dynamically overwrite the function write of the object."""

        def new_write(obj, string):
            print(string)
            # unstable on Windows!!! bad solution... 
            # Have to find something better...
            # self.text.insert(END, string+'\n')
            # self.text.yview_moveto(1)

        # To dynamically overwrite an instance method:
        instancemethod = type(self.obj.write)
        # info on instancemethod:
        # Type:       type
        # String Form:<type 'instancemethod'>
        # Docstring:
        #     instancemethod(function, instance, class)
        #     Create an instance method object.
        self.obj.write = instancemethod(
            new_write, self.obj, self.obj.__class__)





class MyDialogCloseWindow(SimpleDialog):

    def body(self, master):
        question = (
"Do you really want to close the window\n"
"and stop the experiment?")
        self.agree = False
        ttk.Label(master, text=question).grid()
    def apply(self):
        self.agree = True



class MainFrameRunExp(ttk.Frame):
    """"""
    def __init__(self, root=None, exp=None):

        if root is None:
            root = tk.Tk()
        self.root = root
        root.protocol('WM_DELETE_WINDOW', self.ask_if_has_to_be_deleted)

        if exp is not None:
            self._exp = exp

        f = font.nametofont("TkDefaultFont")
        f.configure(size=10)

        f = font.nametofont('TkHeadingFont')
        f.configure(size=14)

        self.root.title('FluidDyn '+__version__)
        ttk.Frame.__init__(self, root, padding="5 5 5 5")
        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frames_objects = {}
        self.create_widgets()


    def create_widgets(self):

        if hasattr(self, '_exp'):
            label_exp = ttk.Label(
                self, text='Experiment:', font='TkHeadingFont')
            label_exp.grid(column=0, row=0, sticky=(W))

            label_exp = ttk.Label(
                self, text=self._exp.name_dir)
            label_exp.grid(column=0, row=0)

        self.clock = ElapsedTimeClock(self, font='TkHeadingFont')
        self.clock.grid(column=0, row=0, sticky=(N, E))

        # self.button_hi = ttk.Button(self)
        # self.button_hi["text"] = "Hello World\n(click me)"
        # self.button_hi["command"] = self.say_hi
        # self.button_hi.grid(padx=10, pady=10)

    # def say_hi(self):
    #     print("hi there, everyone!")

    def add_frame_object(self, obj, **kargs):
        """"""
        self.frames_objects[obj.name] = FrameWritingObject(
            self, obj, **kargs)


    def add_frame_rotating_object(self, obj, **kargs):
        """"""
        self.frames_objects[obj.name] = FrameRotatingObject(
            self, obj, **kargs)




    def mainloop(self):
        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=10)
        ttk.Frame.mainloop(self)


    def ask_if_has_to_be_deleted(self):

        d = MyDialogCloseWindow(self.root)
        if d.agree:
            self.root.destroy()






if __name__ == '__main__':

    from fluiddyn.lab.exp.withconductivityprobe import DaemonMeasureProfiles
    import numpy as np


    def Omega_i(t):
        Omega = 1.
        period = 60
        return Omega/2*( 1 - np.cos(2*np.pi*t/period) )

        # time_rampe = 10
        # t = t/time_rampe
        # if t < Omega:
        #     ret = t*Omega
        # elif t < 2*Omega:
        #     ret = Omega*(2-t)
        # else:
        #     ret = 0
        # return ret

    R_i = 100
    R_o = 482/2
    rc, rt = create_rotating_objects_kepler(Omega_i, R_i, R_o)


    import fluiddyn as fld
    exp = fld.load_exp('Exp_Omega1=0.70_N0=1.80_2014-09-01_23-47-47')






    mainframe = MainFrameRunExp(exp=exp)
    mainframe.add_frame_object(exp.profiles, column=0, row=3)
    mainframe.add_frame_object(rc, column=0, row=4)
    mainframe.add_frame_object(rt, column=0, row=5)






    deamon_profiles = DaemonMeasureProfiles(
        exp=exp, duration=600, period=10, 
        speed_measurements=400, speed_up=100)

    daemon_rc = DaemonRunningRotatingObject(rc)
    daemon_rt = DaemonRunningRotatingObject(rt)

    deamon_profiles.start()

    daemon_rc.start()
    daemon_rt.start()

    mainframe.mainloop()










