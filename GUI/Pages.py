import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
matplotlib.use("TkAgg")

from Models import Cell, Position, MembranePoint, Vesicle
from .NewCell import new_cell_dialog
from .PopupMsg import popupmsg
from .CalculateMSD import MSD_dialog
from .ImportMembrane import membrane_dialog
from .DistanceCacl import distance_dialog


# Definition of generic fonts to use in the pages
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)

# Gestion of the figure
f = Figure()
a = f.add_subplot(111)


# Set initial variables
current_cell = False
hide_membrane = False
filename = ""


# Definition of the starting page, just a warning and basic infos about the app
class StartPage(tk.Frame):

    def __init__(self, parent, controller, session):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=("""Chromaffin cells study application.
        Alpha version.
        Use carefully.
        Consult README to get proper instructions."""))
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Agree",
                             command=lambda: controller.show_frame(CellPage))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree",
                             command=quit)
        button2.pack()


# Definition of the cell page
class CellPage(tk.Frame):

    def __init__(self, parent, controller, session):
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
                             style='my.TButton')
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
        cmb.bind("<<ComboboxSelected>>", lambda _: self.cell_change(
            cmb.get(), session, canvas))
        cmb.pack()
        cell_selection.grid(row=2, column=2)

        var = tk.IntVar()
        check = ttk.Checkbutton(self,
                                text="Hide membrane.",
                                variable=var,
                                command=lambda: self.switch_membrane_vision(
                                    var.get(), session, canvas))
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

        new_cell = ttk.Button(cell_imports,
                              text="Import tracked positions",
                              command=lambda: new_cell_dialog(session))
        calculate_msd = ttk.Button(cell_imports,
                                   text="Calculate the current cell MSDs",
                                   command=lambda: MSD_dialog(session))
        import_membrane_btn = ttk.Button(cell_imports,
                                         text="Import membrane data for a cell",
                                         command=lambda: membrane_dialog(session))
        membrane_dist_btn = ttk.Button(cell_imports,
                                       text="Calculate distance from membrane",
                                       command=lambda: distance_dialog(session))

        label3.grid()
        new_cell.grid(row=2)
        calculate_msd.grid(row=3)
        import_membrane_btn.grid(row=4)
        membrane_dist_btn.grid(row=5)

        cell_imports.grid(row=6, column=2)


    def switch_membrane_vision(self, state, session, canvas):
        global hide_membrane

        hide_membrane = bool(state)
        self.cell_display_update(session, canvas)


    def cell_display_update(self, session, canvas):
        global current_cell

        if current_cell:

            x = []
            y = []

            a.clear()
            vesicles = session.query(Vesicle). \
                filter(Vesicle.cell == current_cell).all()

            for vesicle in vesicles:
                xpos = []
                ypos = []
                positions = session.query(Position). \
                    filter(Position.vesicle == vesicle).all()
                for position in positions:
                    xpos.append(position.x)
                    ypos.append(position.y)

                a.scatter(xpos, ypos)

            if not hide_membrane:
                membrane = session.query(MembranePoint). \
                    filter(MembranePoint.cell == current_cell).all()
                for point in membrane:
                    x.append(point.x)
                    y.append(point.y)
                a.scatter(x, y)

            canvas.draw()

    def cell_change(self, newcell, session, canvas):
        global current_cell

        current_cell = session.query(Cell). \
            filter(Cell.name == newcell).first()
        self.cell_display_update(session, canvas)
