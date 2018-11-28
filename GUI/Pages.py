import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
matplotlib.use("TkAgg")
from Models import Cell, Position, MembranePoint, Vesicle
from Base import Session, engine, Base


# Definition of generic fonts to use in the pages
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)

# Gestion of the figure
f = Figure()
a = f.add_subplot(111)


current_cell = False

# Definition of a simple popup message that closes itself with a button
# Input is the message to display
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="OK", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def vestraj(cell):
    pass


def cell_change(newcell, session, canvas):
    global current_cell

    current_cell = session.query(Cell).filter(Cell.name.contains(newcell[15:])).first()
    animate(session, canvas)


def animate(session, canvas):
    global current_cell

    if current_cell:


        xpos = []
        ypos = []
        a.clear()
        vesicles = session.query(Vesicle).filter(Vesicle.cell == current_cell).all()
        for vesicle in vesicles:
            positions = session.query(Position).filter(Position.vesicle == vesicle).all()
            for position in positions:
                xpos.append(position.x)
                ypos.append(position.y)

            a.scatter(xpos, ypos)
        canvas.draw()




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
        cell_list=[]
        for c in existingcells:
            cell_list.append("..."+c.name[-30:-4])

        cmb = ttk.Combobox(cell_selection, width="30", values=cell_list, state="readonly")
        cmb.bind("<<ComboboxSelected>>", lambda _: cell_change(cmb.get(), session, canvas))
        cmb.pack()
        cell_selection.grid(row=2, column=2)


        """current_cell = session.query(Cell).filter(Cell.name.like(cmb.get())).first()

        cell_info = tk.Frame(self)
        if current_cell:
            cellNameLabel = ttk.Label(cell_info,
                                      text="Cell name: "+current_cell.name)
            cellDateLabel = ttk.Label(cell_info,
                                      text="Experiment date: "+current_cell.date)
            cellStimuLabel = ttk.Label(cell_info,
                                      text="Experiment date: " + current_cell.stimulation_type)
            cellStimuTimeLabel = ttk.Label(cell_info,
                                           text="Experiment date: " + current_cell.stimulation_time)
            cellNameLabel.pack()
            cellDateLabel.pack()
            cellStimuLabel.pack()
            cellStimuTimeLabel.pack()

        cell_info.grid(row=3, column=2)"""


        check = ttk.Checkbutton(self,
                                text="Hide vesicles trajectories.",
                                command=print(cmb.get()))
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
        current_cell = ttk.Label(cell_imports,
                                 text="No current cell",
                                 borderwidth=3,
                                 relief=tk.SUNKEN)
        new_cell = ttk.Button(cell_imports,
                              text="Import tracked positions")
        calculate_msd = ttk.Button(cell_imports,
                                   text="Calculate the current cell MSDs")
        import_membrane = ttk.Button(cell_imports,
                                     text="Import membrane data "
                                          "for the current cell")
        delete_cell = ttk.Button(cell_imports,
                                 text="Delete cell and all related elements")

        label3.grid()
        current_cell.grid(row=1)
        new_cell.grid(row=2)
        calculate_msd.grid(row=3)
        import_membrane.grid(row=4)
        delete_cell.grid(row=5)

        cell_imports.grid(row=6, column=2)




