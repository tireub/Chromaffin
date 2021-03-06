import matplotlib
matplotlib.use("TkAgg")
import matplotlib.animation as animation
from matplotlib import style
import webbrowser
from Base import Session, engine, Base

import tkinter as tk
from tkinter import ttk

from GUI.Pages import CellPage, StartPage, f, VesiclePage, StatsPage
from GUI.PopupMsg import popupmsg


class Chromaffinapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Chromaffin Studies")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Help",
                             command=lambda:
                             webbrowser.open_new("https://github.com/tireub/"
                             "Chromaffin/blob/master/README.md"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, CellPage, VesiclePage, StatsPage):
            frame = F(container, self, session)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # def update_frame(self, cont):




Base.metadata.create_all(engine)
session = Session()
app = Chromaffinapp()
app.geometry("1280x720")
app.minsize(1200, 700)
#ani = animation.FuncAnimation(f, animate, fargs=session, interval=5000)
app.mainloop()
session.close()