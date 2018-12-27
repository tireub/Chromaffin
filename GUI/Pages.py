import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import webbrowser
from tkinter import ttk
from Models import Cell, Position, MembranePoint,\
    Vesicle, MSD, VesicleBehaviour, StimulationType, BehaviourType
from .NewCell import new_cell_dialog
from .PopupMsg import popupmsg
from .CalculateMSD import MSD_dialog
from .ImportMembrane import membrane_dialog
from .DistanceCacl import distance_dialog
from Calculation.BehaviourChanges import behavchange
from Calculation.Changevsoriginalbehaviour import changevsoriginal as chvsori
from Calculation.DistaAtStimuTime import dist_at_stimu as dats
from Calculation.FilterByBehav import filering
mpl.use("TkAgg")

# Definition of generic fonts to use in the pages
SELECTED_FONT = ("Verdana 12 bold")
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
FRAME_TITLE_FONT = ("Verdana 10 bold")
FRAME_IT_FONT = ("Verdana 10 italic")

# Gestion of the figure
f = Figure(facecolor="black")
a = f.add_subplot(111, facecolor="black")
f.subplots_adjust(left=0.05, right=0.85, bottom=0.1, top=0.9)

# Set initial variables
current_cell = False
cell_ves_nbr = 0
filename = ""
current_vesicle = False


# Definition of the starting page, just a warning and basic infos about the app
class StartPage(tk.Frame):

    def __init__(self, parent, controller, session):
        tk.Frame.__init__(self, parent)
        for i in range(2):
            self.columnconfigure(i, weight=1)
        for i in range(3):
            self.rowconfigure(i, weight=1)
        label = tk.Label(self, text=("""Chromaffin cells study application.
        Alpha version."""), font=LARGE_FONT)
        link = tk.Label(self,
                        text='Consult README to get proper instructions.',
                        fg="blue", cursor="hand2", font=LARGE_FONT)
        link.bind("<Button-1>", self.callback)

        label.grid(row=0, columnspan=2, pady=100)
        link.grid(row=1, columnspan=2, pady=100)
        button1 = ttk.Button(self, text="Proceed",
                             command=lambda: controller.show_frame(CellPage))
        button1.grid(row=2, column=0, sticky="NSEW", pady=30, padx=30)

        button2 = ttk.Button(self, text="Quit",
                             command=quit)
        button2.grid(row=2, column=1, sticky="NSEW", pady=30, padx=30)

    def callback(self, event):
        webbrowser.open_new("https://github.com/tireub/"
                            "Chromaffin/blob/master/README.md")


# Definition of the cell page
class CellPage(tk.Frame):

    def __init__(self, parent, controller, session):
        tk.Frame.__init__(self, parent)
        # Grid configuration
        self.columnconfigure(0, minsize=400, weight=1)
        self.columnconfigure(1, minsize=400, weight=1)
        self.columnconfigure(2, minsize=400, weight=1)

        for i in range(8):
            self.rowconfigure(i, weight=1)

        # Adding thumbnails buttons
        s = ttk.Style()
        s.configure('my.TButton', font=LARGE_FONT)
        s.configure('Highlighted.TButton', font=SELECTED_FONT)

        button1 = ttk.Button(self,
                             text="Cell",
                             style='Highlighted.TButton')
        button1.grid(sticky="NSEW")
        button2 = ttk.Button(self,
                             text="Vesicle",
                             command=lambda: controller.show_frame(
                                 VesiclePage),
                             style='my.TButton')
        button2.grid(row=0, column=1, sticky="NSEW")
        button3 = ttk.Button(self, text="Statistics",
                             command=lambda: controller.show_frame(StatsPage),
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
        # Cell selection
        cell_selection = tk.Frame(self)
        label1 = ttk.Label(cell_selection, text="Select desired cell :",
                           font=FRAME_TITLE_FONT)
        label1.pack()
        existingcells = session.query(Cell).all()
        cell_list = []
        for c in existingcells:
            cell_list.append(c.name)

        cmb = ttk.Combobox(cell_selection,
                           width="30",
                           values=cell_list,
                           state="readonly",
                           justify="center")
        cmb.bind("<<ComboboxSelected>>", lambda _: self.cell_change(
            cmb.get(), session, canvas))
        cmb.pack()
        cell_selection.grid(row=1, column=2, pady=(5, 5))

        # Definition of the infos frame
        self.cell_value = tk.StringVar()
        self.ves_nbr = tk.IntVar()
        self.stimu_value = tk.StringVar()
        self.frames_nbr = tk.IntVar()
        self.stimu_frame = tk.IntVar()
        self.cell_value.set("NA")
        self.ves_nbr.set(0)
        self.stimu_value.set("NA")
        self.frames_nbr.set(0)
        self.stimu_frame.set(0)

        infos = tk.Frame(self, borderwidth=5, relief=tk.SUNKEN)
        infos.grid_columnconfigure(0, weight=1)
        infos.grid_columnconfigure(1, weight=1)
        infos.grid_columnconfigure(2, weight=1)
        for i in range(6):
            infos.grid_rowconfigure(i, weight=1)
        infoLabel = ttk.Label(infos, text='Cell informations',
                              font=FRAME_TITLE_FONT)
        ilabel1 = ttk.Label(infos, text='Cell name :', font=FRAME_IT_FONT)
        ilabel2 = ttk.Label(infos, text='Number of vesicles :',
                            font=FRAME_IT_FONT)
        ilabel3 = ttk.Label(infos, text='Type of stimulation :',
                            font=FRAME_IT_FONT)
        ilabel4 = ttk.Label(infos, text='Total number of frames :',
                            font=FRAME_IT_FONT)
        ilabel5 = ttk.Label(infos, text='Stimulation frame :',
                            font=FRAME_IT_FONT)
        info1 = ttk.Label(infos, textvariable=self.cell_value)
        info2 = ttk.Label(infos, textvariable=self.ves_nbr)
        info3 = ttk.Label(infos, textvariable=self.stimu_value)
        info4 = ttk.Label(infos, textvariable=self.frames_nbr)
        info5 = ttk.Label(infos, textvariable=self.stimu_frame)
        infoLabel.grid(row=0, column=0, columnspan=3)
        ilabel1.grid(row=1, column=0)
        info1.grid(row=1, column=1, columnspan=2)
        ilabel2.grid(row=2, column=0)
        info2.grid(row=2, column=1, columnspan=2)
        ilabel3.grid(row=3, column=0)
        info3.grid(row=3, column=1, columnspan=2)
        ilabel4.grid(row=4, column=0)
        info4.grid(row=4, column=1, columnspan=2)
        ilabel5.grid(row=5, column=0)
        info5.grid(row=5, column=1, columnspan=2)

        # Add infos subframe to the main window frame
        infos.grid(row=2, column=2, sticky="NSEW")

        distype = tk.Frame(self)
        typelabel = ttk.Label(distype, text="Change trajectories display ",
                              font=FRAME_TITLE_FONT)
        self.distype = tk.StringVar()
        discmb = ttk.Combobox(distype,
                              width="30",
                              values=["Scatter dots", "Lines"],
                              state="readonly",
                              justify="center")
        discmb.bind("<<ComboboxSelected>>", lambda _: self.disp_change(
            discmb.get(), session, canvas))
        typelabel.grid(row=0)
        discmb.grid(row=1, pady=(5, 5))
        distype.grid(row=3, column=2)

        self.hide_membrane = True

        options = tk.Frame(self)
        var = tk.IntVar()
        var.set(True)
        check = ttk.Checkbutton(options,
                                text="Hide membrane.",
                                variable=var,
                                command=lambda: self.switch_membrane_vision(
                                    var.get(), session, canvas))
        check.grid(row=0)
        options.grid(row=4, column=2)

        # Definition of the filters menu
        filters = tk.Frame(self, borderwidth=5, relief=tk.SUNKEN)
        # Set all the elements
        fb = tk.BooleanVar()
        db = tk.BooleanVar()
        cb = tk.BooleanVar()
        fa = tk.BooleanVar()
        da = tk.BooleanVar()
        ca = tk.BooleanVar()
        fb.set(1)
        db.set(1)
        cb.set(1)
        fa.set(1)
        da.set(1)
        ca.set(1)

        label2 = ttk.Label(filters, text="Filter vesicles by behaviour",
                           font=FRAME_TITLE_FONT)
        before = ttk.Label(filters, text="Before stimulation",
                           font=FRAME_IT_FONT)
        after = ttk.Label(filters, text="After stimulation",
                          font=FRAME_IT_FONT)
        freeb = ttk.Label(filters, text="Free")
        chkfb = ttk.Checkbutton(filters, variable=fb)
        directedb = ttk.Label(filters, text="Directed")
        chkdb = ttk.Checkbutton(filters, variable=db)
        cagedb = ttk.Label(filters, text="Caged")
        chkcb = ttk.Checkbutton(filters, variable=cb)
        freea = ttk.Label(filters, text="Free")
        chkfa = ttk.Checkbutton(filters, variable=fa)
        directeda = ttk.Label(filters, text="Directed")
        chkda = ttk.Checkbutton(filters, variable=da)
        cageda = ttk.Label(filters, text="Caged")
        chkca = ttk.Checkbutton(filters, variable=ca)
        # Position all the elements
        for i in range(6):
            filters.grid_columnconfigure(i, weight=1)
        label2.grid(row=0, column=0, columnspan=5)
        before.grid(row=1, column=0, columnspan=2)
        after.grid(row=1, column=3, columnspan=2)
        freeb.grid(row=2, column=0)
        chkfb.grid(row=2, column=1)
        freea.grid(row=2, column=3)
        chkfa.grid(row=2, column=4)
        directedb.grid(row=3, column=0)
        chkdb.grid(row=3, column=1)
        directeda.grid(row=3, column=3)
        chkda.grid(row=3, column=4)
        cagedb.grid(row=4, column=0)
        chkcb.grid(row=4, column=1)
        cageda.grid(row=4, column=3)
        chkca.grid(row=4, column=4)

        self.filters_on = []
        fil = tk.IntVar()
        filterchck = ttk.Checkbutton(options,
                                     text="Apply filters.",
                                     variable=fil,
                                     command=lambda: self.apply_filters(
                                         fil.get(),
                                         [fb.get(), db.get(), cb.get(),
                                          fa.get(), da.get(), ca.get()],
                                         session, canvas))
        filterchck.grid(row=2)
        # Add filters subframe to the main window frame
        filters.grid(row=5, column=2, sticky="EW")

        # Import functions
        cell_imports = tk.Frame(self, borderwidth=5, relief=tk.RAISED)
        label3 = ttk.Label(cell_imports,
                           text="Import and calculation functions for a cell",
                           font=FRAME_TITLE_FONT)

        new_cell = ttk.Button(cell_imports,
                              text="Import tracked positions",
                              command=lambda: new_cell_dialog(session))
        calculate_msd = ttk.Button(cell_imports,
                                   text="Calculate the current cell MSDs",
                                   command=lambda: MSD_dialog(session))
        import_membrane_btn = ttk.Button(cell_imports,
                                         text="Import membrane"
                                              " data for a cell",
                                         command=lambda: membrane_dialog(
                                             session))
        membrane_dist_btn = ttk.Button(cell_imports,
                                       text="Calculate distance"
                                            " from membrane",
                                       command=lambda: distance_dialog(
                                           session))

        label3.grid()
        new_cell.grid(row=1)
        calculate_msd.grid(row=2)
        import_membrane_btn.grid(row=3)
        membrane_dist_btn.grid(row=4)

        cell_imports.grid(row=6, column=2)

    def apply_filters(self, fil, filters, session, canvas):

        self.filters_on = fil
        self.filt_list = filters
        self.cell_display_update(session, canvas)

    def disp_change(self, distype, session, canvas):

        self.distype = distype
        self.cell_display_update(session, canvas)

    def switch_membrane_vision(self, state, session, canvas):

        self.hide_membrane = bool(state)
        self.cell_display_update(session, canvas)

    def cell_display_update(self, session, canvas):
        global current_cell

        if current_cell:

            x = []
            y = []

            a.clear()
            vesicles = session.query(Vesicle). \
                filter(Vesicle.cell == current_cell).all()
            last_ves = vesicles[-1]
            last_pos = session.query(Position).\
                filter(Position.vesicle == last_ves).all()

            norm = mpl.colors.Normalize(vmin=0, vmax=last_pos[-1].t)
            cmap = mpl.cm.get_cmap('plasma')

            ax = f.add_axes([0.9, 0.06, 0.02, 0.90],
                            title="Time frame", facecolor="w")

            cb = mpl.colorbar.ColorbarBase(ax, cmap='plasma', norm=norm,
                                           orientation="vertical")
            cb.set_label('Time frame', color="white")
            ax.tick_params(colors='white')

            if self.filters_on:
                vesicles = filering(session, self.filt_list, current_cell)

            for vesicle in vesicles:
                xpos = []
                ypos = []
                t = []
                positions = session.query(Position). \
                    filter(Position.vesicle == vesicle).all()
                for position in positions:
                    xpos.append(position.x)
                    ypos.append(position.y)
                    t.append(position.t)

                # Check what type of display is required
                if self.distype == "Lines":
                    for i in range(len(xpos) - 1):
                        a.plot((xpos[i], xpos[i + 1]),
                               (ypos[i], ypos[i + 1]),
                               color=cmap(norm(t[i]))[:3])
                else:
                    a.scatter(xpos, ypos, s=3, c=t, cmap='plasma',
                              norm=norm)

            # Check if the membrane is to be displayed
            if not self.hide_membrane:
                membrane = session.query(MembranePoint). \
                    filter(MembranePoint.cell == current_cell).all()
                for point in membrane:
                    x.append(point.x)
                    y.append(point.y)
                a.scatter(x, y, c='g', s=3)

            # Truncate cell name if needed
            if len(current_cell.name) > 35:
                shortname = current_cell.name[:35] + "..."
            else:
                shortname = current_cell.name

            # Put axes in white
            a.spines['bottom'].set_color("white")
            a.spines['left'].set_color("white")
            a.tick_params(colors='white')
            a.set_title(shortname, color="white")

            # Set parameter to get an equal ratio on both axis,
            # avoiding distortion
            a.set_aspect("equal")

            canvas.draw()

            # Set cell infos
            self.cell_value.set(shortname)
            self.ves_nbr.set(len(current_cell.vesicles))
            self.stimu_value.set(current_cell.stimulation_type.chemical)
            self.frames_nbr.set(last_pos[-1].t)
            self.stimu_frame.set(current_cell.stimulation_time)

    def cell_change(self, newcell, session, canvas):
        global current_cell

        current_cell = session.query(Cell). \
            filter(Cell.name == newcell).first()
        self.cell_display_update(session, canvas)


# Definition of the vesicle page
class VesiclePage(tk.Frame):

    def __init__(self, parent, controller, session):
        tk.Frame.__init__(self, parent)
        # Grid configuration
        self.columnconfigure(0, minsize=200, weight=1)
        self.columnconfigure(1, minsize=200, weight=1)
        self.columnconfigure(2, minsize=200, weight=1)
        self.columnconfigure(3, minsize=200, weight=1)
        self.columnconfigure(4, minsize=200, weight=1)
        self.columnconfigure(5, minsize=200, weight=1)

        self.rowconfigure(0, minsize=50, weight=1)
        self.rowconfigure(1, minsize=200, weight=3)
        self.rowconfigure(2, minsize=200, weight=4)

        # Adding thumbnails buttons
        s = ttk.Style()
        s.configure('my.TButton', font=LARGE_FONT)
        s.configure('Highlighted.TButton', font=SELECTED_FONT)

        button1 = ttk.Button(self,
                             text="Cell",
                             style='my.TButton',
                             command=lambda: controller.show_frame(CellPage))
        button1.grid(columnspan=2, sticky="NSEW")
        button2 = ttk.Button(self,
                             text="Vesicle",
                             style='Highlighted.TButton')
        button2.grid(row=0, column=2, columnspan=2, sticky="NSEW")
        button3 = ttk.Button(self, text="Statistics",
                             command=lambda: controller.show_frame(StatsPage),
                             style='my.TButton')
        button3.grid(row=0, column=4, columnspan=2, sticky="NSEW")

        # Vesicle selection panel
        ves_selection = tk.Frame(self)

        label1 = ttk.Label(ves_selection,
                           text="Select desired cell :",
                           font=FRAME_TITLE_FONT)
        label1.grid(row=0, column=0, columnspan=4, pady=(10, 0))
        existingcells = session.query(Cell).all()
        cell_list = []
        for c in existingcells:
            cell_list.append(c.name)

        cmb = ttk.Combobox(ves_selection,
                           width="30",
                           values=cell_list,
                           state="readonly",
                           justify="center")
        cmb.bind("<<ComboboxSelected>>", lambda _: self.cell_change(cmb.get(),
                                                                    session))
        cmb.grid(row=1, column=0, columnspan=4, pady=(0, 25))
        vesLabel = ttk.Label(ves_selection,
                             text="Select desired vesicle :",
                             font=FRAME_TITLE_FONT)
        prevButton = ttk.Button(ves_selection,
                                text='Previous',
                                command=lambda: self.ves_update(
                                    session, "Previous"),
                                style='my.TButton')
        nextButton = ttk.Button(ves_selection,
                                text='Next',
                                command=lambda: self.ves_update(
                                    session, "Next"),
                                style='my.TButton')
        self.veschoice = tk.StringVar()
        vesnbr = ttk.Entry(ves_selection,
                           textvariable=self.veschoice,
                           justify="center")
        choosebtn = ttk.Button(ves_selection,
                               text="Set vesicle number",
                               command=lambda: self.ves_update(
                                   session, vesnbr.get()),
                               style='my.TButton')
        vesLabel.grid(row=2, column=0, columnspan=4)
        prevButton.grid(row=3, column=1, sticky="EW", padx=(5, 5), pady=(5, 5))
        nextButton.grid(row=3, column=3, sticky="EW", padx=(5, 5), pady=(5, 5))
        vesnbr.grid(row=3, column=2, sticky="EW", padx=(5, 5), pady=(5, 5))
        choosebtn.grid(row=4, column=2)

        ves_selection.grid(row=1, column=0, columnspan=3)

        # Vesicle trajectory figure initialisation
        self.vesfig = Figure(facecolor="black")
        self.trajplot = self.vesfig.add_subplot(111, facecolor="black")
        self.trajcanvas = FigureCanvasTkAgg(self.vesfig, self)
        self.trajcanvas.draw()
        self.trajcanvas.get_tk_widget().grid(row=2, column=0,
                                             columnspan=2, sticky="NSEW")
        # MSD fit before stimu figure initialisation
        self.msdbef = Figure()
        self.msdbefplot = self.msdbef.add_subplot(111)
        self.msdbefcanv = FigureCanvasTkAgg(self.msdbef, self)
        self.msdbefcanv.draw()
        self.msdbefcanv.get_tk_widget().grid(row=2, column=2, columnspan=2,
                                             sticky="NSEW")

        # MSD fit after stimu figure initialisation
        self.msdaft = Figure()
        self.msdaftplot = self.msdaft.add_subplot(111)
        self.msdaftcanv = FigureCanvasTkAgg(self.msdaft, self)
        self.msdaftcanv.draw()
        self.msdaftcanv.get_tk_widget().grid(row=2, column=4, columnspan=2,
                                             sticky="NSEW")

        # Definition of the infos menu
        self.cell_value = tk.StringVar()
        self.ves_value = tk.IntVar()
        self.points_value = tk.IntVar()
        self.bef_value = tk.StringVar()
        self.aft_value = tk.StringVar()
        self.cell_value.set("NA")
        self.ves_value.set(0)
        self.points_value.set(0)
        self.bef_value.set("NA")
        self.aft_value.set("NA")

        infos = tk.Frame(self, borderwidth=5, relief=tk.SUNKEN)
        infos.grid_columnconfigure(0, weight=1)
        infos.grid_columnconfigure(1, weight=1)
        infos.grid_columnconfigure(2, weight=1)
        for i in range(6):
            infos.grid_rowconfigure(i, weight=1)
        infoLabel = ttk.Label(infos,
                              text='Vesicle informations',
                              font=FRAME_TITLE_FONT)
        ilabel1 = ttk.Label(infos, text='Cell name :', font=FRAME_IT_FONT)
        ilabel2 = ttk.Label(infos, text='Vesicle number :', font=FRAME_IT_FONT)
        ilabel3 = ttk.Label(infos, text='Number of points :',
                            font=FRAME_IT_FONT)
        ilabel4 = ttk.Label(infos,
                            text='Behaviour before stimulation :',
                            font=FRAME_IT_FONT)
        ilabel5 = ttk.Label(infos,
                            text='Behaviour before stimulation :',
                            font=FRAME_IT_FONT)
        info1 = ttk.Label(infos, textvariable=self.cell_value)
        info2 = ttk.Label(infos, textvariable=self.ves_value)
        info3 = ttk.Label(infos, textvariable=self.points_value)
        info4 = ttk.Label(infos, textvariable=self.bef_value)
        info5 = ttk.Label(infos, textvariable=self.aft_value)
        infoLabel.grid(row=0, columnspan=3)
        ilabel1.grid(row=1, column=0)
        info1.grid(row=1, column=1)
        ilabel2.grid(row=2, column=0)
        info2.grid(row=2, column=1)
        ilabel3.grid(row=3, column=0)
        info3.grid(row=3, column=1)
        ilabel4.grid(row=4, column=0)
        info4.grid(row=4, column=1)
        ilabel5.grid(row=5, column=0)
        info5.grid(row=5, column=1)

        # Add infos subframe to the main window frame
        infos.grid(row=1, column=3, columnspan=3, sticky="NSEW")

    # Actions to apply when a new cell is selected from the combobox
    def cell_change(self, newcell, session):
        global current_cell
        global current_vesicle
        global cell_ves_nbr

        current_cell = session.query(Cell). \
            filter(Cell.name == newcell).first()
        current_vesicle = 0
        cell_ves_nbr = len(
            session.query(Vesicle).filter(Vesicle.cell == current_cell).all())
        self.ves_display_update(session)

    # Any change of the vesicle to display
    def ves_update(self, session, command):
        global current_vesicle

        # Test if there is a current cell to which we can study the vesicles
        if not current_cell:
            popupmsg("Please select a cell before trying to select a vesicle")

        else:
            if command == "Next":
                if current_vesicle < cell_ves_nbr - 1:
                    current_vesicle = current_vesicle + 1

            elif command == "Previous":
                if current_vesicle > 0:
                    current_vesicle = current_vesicle - 1

            else:
                # Check if the entry is actually an integer
                try:
                    val = int(command)
                    if val < 1:
                        current_vesicle = 0
                    elif val >= cell_ves_nbr + 1:
                        current_vesicle = cell_ves_nbr - 1
                    else:
                        current_vesicle = val - 1

                except:
                    popupmsg("Please enter an integer value.")

        self.ves_display_update(session)
        self.veschoice.set(current_vesicle + 1)

    def ves_display_update(self, session):
        vesicles = \
            session.query(Vesicle).filter(Vesicle.cell == current_cell).all()

        last_ves = vesicles[-1]
        last_pos = session.query(Position). \
            filter(Position.vesicle == last_ves).all()
        norm = mpl.colors.Normalize(vmin=0, vmax=last_pos[-1].t)
        cmap = mpl.cm.get_cmap('plasma')
        ax = self.vesfig.add_axes([0.89, 0.06, 0.02, 0.90], "Time frame")
        ax.tick_params(colors='white')
        cb = mpl.colorbar.ColorbarBase(ax, cmap='plasma', norm=norm,
                                       orientation="vertical")

        ves = vesicles[current_vesicle]

        # Update the first plot, vesicle traj
        self.trajplot.clear()
        xpos = []
        ypos = []
        t = []

        positions = session.query(Position).filter(
            Position.vesicle == ves).all()
        for position in positions:
            xpos.append(position.x)
            ypos.append(position.y)
            t.append(position.t)

        for i in range(len(xpos)-1):
            self.trajplot.plot((xpos[i], xpos[i + 1]),
                               (ypos[i], ypos[i + 1]),
                               'o-',
                               color=cmap(norm(t[i]))[:3])

        # Configuration of axis, and label, conserving ration axis
        self.trajplot.spines['bottom'].set_color("white")
        self.trajplot.spines['left'].set_color("white")
        self.trajplot.tick_params(colors='white')
        self.trajplot.set_title("Vesicle positions", color="white")
        self.trajplot.set_aspect("equal")

        self.trajcanvas.draw()

        # Update the msdbefore figure
        self.msdbefplot.clear()
        dt = []
        y = []
        values = session.query(MSD).filter(MSD.vesicle == ves,
                                           MSD.before_after_stimu == 1).all()
        for value in values:
            dt.append(float(value.deltat))
            y.append(float(value.value))
        self.msdbefplot.scatter(dt, y)
        if len(dt) > 3:
            fit = np.polyfit(dt, y, 2)
            fits = [fit[0]*i**2 + fit[1]*i for i in dt]
            self.msdbefplot.plot(dt, fits)
        self.msdbefplot.set_title("MSD before stimulation")
        self.msdbefplot.set_xlabel("Delta T")
        self.msdbefcanv.draw()

        # Update the MSDaft figure
        self.msdaftplot.clear()
        dt = []
        y = []
        values = session.query(MSD).filter(MSD.vesicle == ves,
                                           MSD.before_after_stimu == 2).all()
        for value in values:
            dt.append(float(value.deltat))
            y.append(float(value.value))
        self.msdaftplot.scatter(dt, y)

        if len(dt) > 3:
            fit = np.polyfit(dt, y, 2)
            fits = [fit[0] * i ** 2 + fit[1] * i for i in dt]
            self.msdaftplot.plot(dt, fits)
        self.msdaftplot.set_title("MSD after stimulation")
        self.msdaftplot.set_xlabel("Delta T")
        self.msdaftcanv.draw()

        # Update the right panel values
        # Truncate cell name if needed
        if len(current_cell.name) > 35:
            shortname = current_cell.name[:35] + "..."
        else:
            shortname = current_cell.name
        self.cell_value.set(shortname)
        self.ves_value.set(current_vesicle+1)
        self.points_value.set(ves.track_duration)
        try:
            behavbef = session.query(VesicleBehaviour).filter(
                VesicleBehaviour.vesicle == ves,
                VesicleBehaviour.time_status == 1).first().behaviour_type.type
            self.bef_value.set(behavbef)
        except:
            self.bef_value.set("NA")
        try:
            behavaft = session.query(VesicleBehaviour).filter(
                VesicleBehaviour.vesicle == ves,
                VesicleBehaviour.time_status == 2).first().behaviour_type.type
            self.aft_value.set(behavaft)
        except:
            self.aft_value.set("NA")

        # Update ves navigation value
        self.veschoice.set(current_vesicle + 1)


class StatsPage(tk.Frame):

    def __init__(self, parent, controller, session):
        tk.Frame.__init__(self, parent)
        # Grid configuration
        self.columnconfigure(0, minsize=200, weight=1)
        self.columnconfigure(1, minsize=200, weight=1)
        self.columnconfigure(2, minsize=200, weight=1)
        self.columnconfigure(3, minsize=200, weight=1)
        self.columnconfigure(4, minsize=200, weight=1)
        self.columnconfigure(5, minsize=200, weight=1)

        self.rowconfigure(0, minsize=40, weight=1)
        self.rowconfigure(1, minsize=150, weight=3)
        self.rowconfigure(2, minsize=100, weight=3)
        self.rowconfigure(3, minsize=50, weight=2)
        self.rowconfigure(4, minsize=50, weight=2)
        self.rowconfigure(5, minsize=50, weight=2)

        # Adding thumbnails buttons
        s = ttk.Style()
        s.configure('my.TButton', font=LARGE_FONT)
        s.configure('Highlighted.TButton', font=SELECTED_FONT)

        button1 = ttk.Button(self,
                             text="Cell",
                             style='my.TButton',
                             command=lambda: controller.show_frame(CellPage))
        button1.grid(columnspan=2, sticky="NSEW")
        button2 = ttk.Button(self,
                             text="Vesicle",
                             style='my.TButton',
                             command=lambda: controller.show_frame(
                                 VesiclePage))
        button2.grid(row=0, column=2, columnspan=2, sticky="NSEW")
        button3 = ttk.Button(self, text="Statistics",
                             style='Highlighted.TButton')
        button3.grid(row=0, column=4, columnspan=2, sticky="NSEW")

        self.stat_type = tk.StringVar()
        self.stimu_type = tk.StringVar()
        self.all_cells = tk.BooleanVar()
        self.cell_num = tk.IntVar()
        self.ves_num = tk.IntVar()
        self.filter = tk.IntVar()

        # Subframe summarising what is displayed
        summary = tk.Frame(self, borderwidth=5, relief=tk.SUNKEN)
        for i in range(6):
            summary.rowconfigure(i, weight=1)
        summary.columnconfigure(0, weight=1)
        summary.columnconfigure(1, weight=1)
        slabel1 = ttk.Label(summary, text='Statistics displayed :',
                            font=FRAME_IT_FONT)
        info1 = ttk.Label(summary, textvariable=self.stat_type,
                          font=FRAME_TITLE_FONT)
        slabel2 = ttk.Label(summary, text='Type of stimulation :',
                            font=FRAME_IT_FONT)
        info2 = ttk.Label(summary, textvariable=self.stimu_type)
        slabel3 = ttk.Label(summary, text='All cells included :',
                            font=FRAME_IT_FONT)
        info3 = ttk.Label(summary, textvariable=self.all_cells)
        slabel4 = ttk.Label(summary, text='Number of cells :',
                            font=FRAME_IT_FONT)
        info4 = ttk.Label(summary, textvariable=self.cell_num)
        slabel5 = ttk.Label(summary, text='Number of vesicles :',
                            font=FRAME_IT_FONT)
        info5 = ttk.Label(summary, textvariable=self.ves_num)
        exportbutton = ttk.Button(summary, text='Export graph')
        slabel1.grid()
        slabel2.grid(row=1)
        slabel3.grid(row=2)
        slabel4.grid(row=3)
        slabel5.grid(row=4)
        info1.grid(row=0, column=1)
        info2.grid(row=1, column=1)
        info3.grid(row=2, column=1)
        info4.grid(row=3, column=1)
        info5.grid(row=4, column=1)
        exportbutton.grid(row=5, columnspan=2)
        summary.grid(row=1, columnspan=2, sticky="NSEW")

        # Subframe to select options for the filters
        stats_options = tk.Frame(self)

        type_label = ttk.Label(stats_options,
                               text="Select the stimulation type :")
        stimutypes = session.query(StimulationType).all()
        stimu_list = []
        for c in stimutypes:
            stimu_list.append(c.chemical)

        cmb = ttk.Combobox(stats_options,
                           width="30",
                           values=stimu_list,
                           state="readonly")
        cmb.bind("<<ComboboxSelected>>")
        type_label.grid(row=0, pady=(10, 20))
        cmb.grid(row=0, column=1, pady=(10, 20))
        selectcells = ttk.Button(stats_options,
                                 text="Chose cells to remove",
                                 command=lambda: popupmsg(
                                     "Not supported yet!"))
        remove = ttk.Checkbutton(stats_options,
                                 variable=self.filter,
                                 text="Remove selected cells")
        selectcells.grid(row=1, pady=(10, 10))
        remove.grid(row=1, column=1, pady=(10, 10))
        oriLabel = ttk.Label(stats_options, text="Select original behaviour :")
        behav = session.query(BehaviourType).all()
        behav_list = []
        for b in behav:
            behav_list.append(b.type)
        original = ttk.Combobox(stats_options,
                                width="30",
                                values=behav_list,
                                state="readonly")
        original.bind("<<ComboboxSelected>>")
        oriLabel.grid(row=2, pady=(20, 10))
        original.grid(row=2, column=1, pady=(20, 10))
        stats_options.grid(row=2, columnspan=2)

        # Adding the display options buttons
        popButton = ttk.Button(self,
                               text="Population changes",
                               style="my.TButton",
                               command=lambda: self.popchange_display(
                                   session, cmb.get()))
        switchButton = ttk.Button(self,
                                  text="Changes vs initial behaviour",
                                  style="my.TButton",
                                  command=lambda: self.ch_vs_ori_display(
                                      session,
                                      cmb.get(),
                                      original.get()))
        distButton = ttk.Button(self,
                                text="Changes vs distance to membrane",
                                style="my.TButton",
                                command=lambda: self.nine_quadrants_display(
                                    session, cmb.get()))
        popButton.grid(row=3, columnspan=2, sticky="NSEW")
        switchButton.grid(row=4, columnspan=2, sticky="NSEW")
        distButton.grid(row=5, columnspan=2, sticky="NSEW")

        # Stats plots initialisation
        self.statsfig = Figure()
        # self.popsplot = self.statsfig.add_subplot(111)
        self.statcanvas = FigureCanvasTkAgg(self.statsfig, self)
        self.statcanvas.draw()
        self.statcanvas.get_tk_widget().grid(row=1, rowspan=5, column=2,
                                             columnspan=4, sticky="NSEW")

    def popchange_display(self, session, stimu):
        if not stimu:
            popupmsg("Please select a stimulation type "
                     "before trying to get statistics.")
        else:
            self.statsfig.clear()
            self.popsplot = self.statsfig.add_subplot(111)
            (fb, db, cb,
             fa, da, ca, cellnbr, vesnbr) = behavchange(session, stimu)

            # Edit informations
            self.stat_type.set("Change in populations")
            self.stimu_type.set(stimu)
            self.all_cells.set(not self.filter.get())
            self.cell_num.set(cellnbr)
            self.ves_num.set(vesnbr)

            # data
            before = [fb, db, cb]
            after = [fa, da, ca]

            labels = ("Free", "Directed", "Caged")
            y_pos = np.arange(len(labels))

            bar_width = 0.35
            opacity = 0.8
            labels = ("", "Free", "", "Directed", "", "Caged")
            b = self.popsplot.bar(y_pos, before, bar_width,
                                  label='Before', align='center')
            b[0].set_color('#00CC00')
            b[1].set_color('#99CCFF')
            b[2].set_color('#FF6666')
            a = self.popsplot.bar(y_pos + bar_width, after, bar_width,
                                  label='After')
            a[0].set_color('g')
            a[1].set_color('b')
            a[2].set_color('r')
            self.popsplot.axes.set_xticklabels(labels,
                                               fontdict=None,
                                               minor=False)
            self.popsplot.axes.tick_params(axis='x',
                                           which='both',
                                           bottom=False,
                                           top=False)
            self.popsplot.axes.set_title("Populations percentage changes")

            self.statcanvas.draw()

    def ch_vs_ori_display(self, session, stimu, original):
        if not stimu:
            popupmsg("Please select a stimulation type "
                     "before trying to get statistics.")

        elif not original:
            popupmsg("Please select an original behaviour "
                     "before trying to get statistics.")

        else:
            self.statsfig.clear()
            self.popsplot = self.statsfig.add_subplot(111)
            (newfree, newdir, newcaged, calc, cellnbr) = chvsori(session,
                                                                 stimu,
                                                                 original)

            # Edit informations
            self.stat_type.set(original + " vesicles new behaviour")
            self.stimu_type.set(stimu)
            self.all_cells.set(not self.filter.get())
            self.cell_num.set(cellnbr)
            self.ves_num.set(len(newfree) + len(newdir) + len(newcaged))

            if calc:
                sum = len(newfree) + len(newdir) + len(newcaged)
                nfper = len(newfree) / sum
                ndper = len(newdir) / sum
                ncper = len(newcaged) / sum
            else:
                nfper = 0
                ndper = 0
                ncper = 0

            title = original + " vesicles new behaviour"
            labels = ("Free", "Directed", "Caged")
            y_pos = np.arange(len(labels))
            values = [nfper, ndper, ncper]
            bar = self.popsplot.bar(y_pos, values, align='center')
            bar[0].set_color('g')
            bar[2].set_color('r')
            labels = ("", "", "Free", "", "Directed", "", "Caged")
            self.popsplot.axes.set_xticklabels(labels,
                                               fontdict=None,
                                               minor=False)
            self.popsplot.axes.tick_params(axis='x',
                                           which='both',
                                           bottom=False,
                                           top=False)
            self.popsplot.axes.set_title(title)

            self.statcanvas.draw()

    def nine_quadrants_display(self, session, stimu):
        if not stimu:
            popupmsg("Please select a stimulation type "
                     "before trying to get statistics.")
        else:
            self.statsfig.clear()
            bins = np.linspace(0, 7, 15)

            vestotal = 0

            # Originally free
            (newfree, newdir, newcaged, calc, cellnbr) = chvsori(session,
                                                                 stimu,
                                                                 "Free")

            self.ffsplot = self.statsfig.add_subplot(331)
            distances = dats(session, newfree)
            vestotal += (len(distances))
            self.ffsplot.hist(distances, bins, color="g")
            self.ffsplot.axes.set_title("F2F")
            self.fdsplot = self.statsfig.add_subplot(332)
            distances = dats(session, newdir)
            vestotal += (len(distances))
            self.fdsplot.hist(distances, bins)
            self.fdsplot.axes.set_title("F2D")
            self.fcsplot = self.statsfig.add_subplot(333)
            distances = dats(session, newcaged)
            vestotal += (len(distances))
            self.fcsplot.hist(distances, bins, color="r")
            self.fcsplot.axes.set_title("F2C")

            # Originally directed
            (newfree, newdir, newcaged, calc, cellnbr) = chvsori(session,
                                                                 stimu,
                                                                 "Directed")

            self.dfsplot = self.statsfig.add_subplot(334)
            distances = dats(session, newfree)
            vestotal += (len(distances))
            self.dfsplot.hist(distances, bins, color="g")
            self.dfsplot.axes.set_title("D2F")
            self.ddsplot = self.statsfig.add_subplot(335)
            distances = dats(session, newdir)
            vestotal += (len(distances))
            self.ddsplot.hist(distances, bins)
            self.ddsplot.axes.set_title("D2D")
            self.dcsplot = self.statsfig.add_subplot(336)
            distances = dats(session, newcaged)
            vestotal += (len(distances))
            self.dcsplot.hist(distances, bins, color="r")
            self.dcsplot.axes.set_title("D2C")

            # Originally caged
            (newfree, newdir, newcaged, calc, cellnbr) = chvsori(session,
                                                                 stimu,
                                                                 "Caged")

            self.cfsplot = self.statsfig.add_subplot(337)
            distances = dats(session, newfree)
            vestotal += (len(distances))
            self.cfsplot.hist(distances, bins, color="g")
            self.cfsplot.axes.set_title("C2F")
            self.cdsplot = self.statsfig.add_subplot(338)
            distances = dats(session, newdir)
            vestotal += (len(distances))
            self.cdsplot.hist(distances, bins)
            self.cdsplot.axes.set_title("C2D")
            self.ccsplot = self.statsfig.add_subplot(339)
            distances = dats(session, newcaged)
            vestotal += (len(distances))
            self.ccsplot.hist(distances, bins, color="r")
            self.ccsplot.axes.set_title("C2C")

            self.statsfig.tight_layout()
            self.statcanvas.draw()

            # Edit informations
            self.stat_type.set("Switch distance")
            self.stimu_type.set(stimu)
            self.all_cells.set(not self.filter.get())
            self.cell_num.set(cellnbr)
            self.ves_num.set(vestotal)
