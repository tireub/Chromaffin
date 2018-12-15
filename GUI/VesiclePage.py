import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk

from .PopupMsg import popupmsg

from Models import Cell

"""
# Definition of generic fonts to use in the pages
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)

# Gestion of the figure
f = Figure(facecolor="black")
a = f.add_subplot(111, facecolor="black")

# Definition of the vesicle page
class VesiclePage(tk.Frame):

    def __init__(self, parent, controller, session, CellPage):
        tk.Frame.__init__(self, parent)
        # Grid configuration
        self.columnconfigure(0, minsize=400, weight=1)
        self.columnconfigure(1, minsize=400, weight=1)
        self.columnconfigure(2, minsize=400, weight=1)

        for i in range(7):
            self.rowconfigure(i, weight=1)

        # Adding thumbnails buttons
        s = ttk.Style()
        s.configure('my.TButton', font=LARGE_FONT)

        button1 = ttk.Button(self,
                             text="Cell",
                             style='my.TButton',
                             command=lambda: controller.show_frame(CellPage))
        button1.grid(sticky="NSEW")
        button2 = ttk.Button(self,
                             text="Vesicle",
                             command=lambda: popupmsg(
                                 "Not supported yet!"),
                             style='my.TButton')
        button2.grid(row=0, column=1, sticky="NSEW")
        button3 = ttk.Button(self, text="Statistics",
                             command=lambda: popupmsg(
                                 "Not supported yet!"),
                             style='my.TButton')
        button3.grid(row=0, column=2, sticky="NSEW")

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, rowspan=6, column=0,
                                    columnspan=2, sticky="NSEW")
        toolbarFrame = tk.Frame(master=self)
        toolbarFrame.grid(row=7, column=0, columnspan=2)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

        # Definition of the interaction functions
        cell_selection = tk.Frame(self)
        label1 = ttk.Label(cell_selection, text="Select desired cell :")
        label1.pack()
        existingcells = session.query(Cell).all()
        cell_list = []
        for c in existingcells:
            cell_list.append(c.name)

        cmb = ttk.Combobox(cell_selection,
                           width="30",
                           values=cell_list,
                           state="readonly")
        cmb.bind("<<ComboboxSelected>>")
        cmb.pack()
        cell_selection.grid(row=2, column=2)

        var = tk.IntVar()
        check = ttk.Checkbutton(self,
                                text="Hide membrane.",
                                variable=var,
                                )
        check.grid(row=4, column=2)

        # Definition of the filters menu
        filters = tk.Frame(self, borderwidth=5, relief=tk.SUNKEN)
        # Set all the elements
        label2 = ttk.Label(filters, text="Filter vesicles by behaviour")
        before = ttk.Label(filters, text="Before stimulation")
        after = ttk.Label(filters, text="After stimulation")
        directedb = ttk.Label(filters, text="Directed")
        db = ttk.Checkbutton(filters)
        freeb = ttk.Label(filters, text="Free")
        fb = ttk.Checkbutton(filters)
        cagedb = ttk.Label(filters, text="Caged")
        cb = ttk.Checkbutton(filters)
        directeda = ttk.Label(filters, text="Directed")
        da = ttk.Checkbutton(filters)
        freea = ttk.Label(filters, text="Free")
        fa = ttk.Checkbutton(filters)
        cageda = ttk.Label(filters, text="Caged")
        ca = ttk.Checkbutton(filters)
        # Position all the elements
        label2.grid(columnspan=5)
        before.grid(row=1, column=0, columnspan=2)
        after.grid(row=1, column=3, columnspan=2)
        directedb.grid(row=2, column=0)
        db.grid(row=2, column=1)
        directeda.grid(row=2, column=3)
        da.grid(row=2, column=4)
        freeb.grid(row=3, column=0)
        fb.grid(row=3, column=1)
        freea.grid(row=3, column=3)
        fa.grid(row=3, column=4)
        cagedb.grid(row=4, column=0)
        cb.grid(row=4, column=1)
        cageda.grid(row=4, column=3)
        ca.grid(row=4, column=4)
        # Add filters subframe to the main window frame
        filters.grid(row=5, column=2, sticky="EW")

        # Import functions
        cell_imports = tk.Frame(self, borderwidth=5, relief=tk.RAISED)
        label3 = ttk.Label(cell_imports,
                           text="Import and calculation functions for a cell")



        label3.grid()


        cell_imports.grid(row=6, column=2)"""

# Check wich color scheme to display (magma points, linear timecoded, behaviour colored)

# Extract all vesicles

# If filters = 1
# For each vesicle, check if we display it
# Display it with the proper color code



# Continuous color lines display:
""" 
xpos = []
ypos = []
t = []
    
    positions = session.query(Position). filter(Position.vesicle == vesicle).all()
    for position in positions:
        xpos.append(position.x)
        ypos.append(position.y)
        t.append(position.t)

    norm = mpl.colors.Normalize(vmin=0, vmax=t[-1)
    ax = f.add_axes([0.9, 0.06, 0.02, 0.90], "Time frame")
    cb = mpl.colorbar.ColorbarBase(ax, cmap='magma', norm=norm,
                                           orientation="vertical")
    cb.set_label('Time frame')

    for i in len(xpos) - 1:
        plot(xpos[i:i+1], y[i:i+1], c=norm(t[i])
        
            
"""

# Filter option:

# Filter is a self.filter boolean
"""
a.clear()
            vesicles = session.query(Vesicle). \
                filter(Vesicle.cell == current_cell).all()
            last_ves = vesicles[-1]
            last_pos = session.query(Position).\
                filter(Position.vesicle == last_ves).all()"""

