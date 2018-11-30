import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, HORIZONTAL, END, filedialog
matplotlib.use("TkAgg")
from Models import Cell, Position, MembranePoint, Vesicle, StimulationType
from Base import Session, engine, Base
from Imports.Imports import cell_import
from Calculation.MSDCalc import CellMSDs
from Calculation.BehaviourSorting import cellSorting


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

"""def progressmsg(l):
    pop = tk.Tk()
    pop.wm_title("Progress")
    label = ttk.Label(pop, text="Working...", font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    p = ttk.Progressbar(pop, orient=HORIZONTAL, length=l, mode='determinate')
    p.pack()
    pop.mainloop()"""

def vestraj(cell):
    pass

def browse_file(entrytofill):
    global filename

    filename = filedialog.askopenfilename()
    entrytofill.delete(0, END)
    entrytofill.insert(0, filename)

# Import function called from dialog box
def import_cell(dialog, session, filepath, msd, sort, name, date, stimutime, type):
    print(filepath, msd, sort, name, date, stimutime, type)
    if not session.query(Cell).filter(Cell.name == name):
        cell_import(session, filepath, name, date, stimutime, type)

    if msd:
        cell = session.query(Cell).filter(Cell.name == name).first()
        CellMSDs(session, cell)

        if sort:
            cellSorting(session, cell)
    dialog.destroy()


# Dialog box for new cell import
def new_cell_dialog(session):

    dialog = tk.Toplevel()
    dialog.minsize(400,300)
    dialog.wm_title("Import new cell data")
    label = ttk.Label(dialog, text="Choose file location:")
    txt = ttk.Entry(dialog, width=50)
    browse = ttk.Button(dialog, text="Browse", command= lambda: browse_file(txt))
    label.grid(column=0,columnspan=2)
    txt.grid(row=1)
    browse.grid(row=1, column=1)

    # Infos of the cell, needed to have nice import
    infos = tk.Frame(dialog)
    warning = ttk.Label(infos, text="Please fill these infos carefully")
    label4 = ttk.Label(infos, text="Cell name : ")
    name_entry = ttk.Entry(infos, width=20)
    label5 = ttk.Label(infos, text="Date (YYYY-MM-DD : ")
    date_entry = ttk.Entry(infos, width=10)
    label6 = ttk.Label(infos, text="Stimulation frame :")
    stimu_time_entry = ttk.Entry(infos, width=3)
    stimutypes = session.query(StimulationType).all()
    label7 = ttk.Label(infos, text="Stimulation type : ")
    types_list = []
    for t in stimutypes:
        types_list.append(t.chemical)

    stimu_type = ttk.Combobox(infos,
                           width="30",
                           values=types_list,
                           state="readonly")
    # Elements disposition within the window
    warning.grid(row=0, column=0, columnspan=2)
    label4.grid(row=1, column=0)
    name_entry.grid(row=1, column=1)
    label5.grid(row=2, column=0)
    date_entry.grid(row=2, column=1)
    label6.grid(row=3, column=0)
    stimu_time_entry.grid(row=3, column=1)
    label7.grid(row=4, column=0)
    stimu_type.grid(row=4, column=1)
    infos.grid(row=2, columnspan=2)

    # Calculation options
    option = tk.Frame(dialog)
    label2 = ttk.Label(option, text="Calculate MSD ?")
    msd = tk.BooleanVar()
    chkbx = tk.Checkbutton(option, variable=msd)
    label2.grid()
    chkbx.grid(row=0, column=1)
    label3 = ttk.Label(option, text="Sort behaviour ?")
    sort = tk.BooleanVar()
    chkbx2 = tk.Checkbutton(option, variable=sort)
    label3.grid(row=1)
    chkbx2.grid(row=1, column=1)
    option.grid(row=3, columnspan=2)

    validate = ttk.Button(dialog,
                          text="Import",
                          command=lambda : import_cell(dialog,
                                                       session,
                                                       txt.get(),
                                                       msd.get(),
                                                       sort.get(),
                                                       name_entry.get(),
                                                       date_entry.get(),
                                                       stimu_time_entry.get(),
                                                       stimu_type.get()))
    validate.grid(row=4, columnspan=2)


# Update the cell to be displayed
def cell_change(parent, newcell, session, canvas):
    global current_cell

    current_cell = session.query(Cell).\
        filter(Cell.name == newcell).first()
    cell_display_update(parent, session, canvas)

# Update the membrane vision state
def switch_membrane_vision(parent, state, session, canvas):
    global hide_membrane

    hide_membrane = bool(state)
    cell_display_update(parent, session, canvas)

# Updates the matplotlib window
def cell_display_update(parent, session, canvas):
    global current_cell

    if current_cell:

        x=[]
        y=[]

        a.clear()
        vesicles = session.query(Vesicle).\
            filter(Vesicle.cell == current_cell).all()
        # p = ttk.Progressbar(parent, orient=HORIZONTAL, length=len(vesicles),
        #                    mode='determinate')
        # p.grid(row=3, column=2)
        for vesicle in vesicles:
            xpos = []
            ypos = []
            positions = session.query(Position).\
                filter(Position.vesicle == vesicle).all()
            for position in positions:
                xpos.append(position.x)
                ypos.append(position.y)

            a.scatter(xpos, ypos)
            # p.step()

        if not hide_membrane:
            membrane = session.query(MembranePoint).\
                filter(MembranePoint.cell == current_cell).all()
            for point in membrane:
                x.append(point.x)
                y.append(point.y)
            a.scatter(x,y)

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
            cell_list.append(c.name)

        cmb = ttk.Combobox(cell_selection,
                           width="30",
                           values=cell_list,
                           state="readonly")
        cmb.bind("<<ComboboxSelected>>", lambda _: cell_change(
            self, cmb.get(), session, canvas))
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

        var = tk.IntVar()
        check = ttk.Checkbutton(self,
                                text="Hide membrane.",
                                variable = var,
                                command=lambda : switch_membrane_vision(
                                    self, var.get(), session, canvas))
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
                              command= lambda :new_cell_dialog(session))
        calculate_msd = ttk.Button(cell_imports,
                                   text="Calculate the current cell MSDs")
        import_membrane = ttk.Button(cell_imports,
                                     text="Import membrane data "
                                          "for the current cell")
        delete_cell = ttk.Button(cell_imports,
                                 text="Delete cell and all related elements")

        label3.grid()
        new_cell.grid(row=2)
        calculate_msd.grid(row=3)
        import_membrane.grid(row=4)
        delete_cell.grid(row=5)

        cell_imports.grid(row=6, column=2)




