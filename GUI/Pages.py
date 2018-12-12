import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
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
mpl.use("TkAgg")

# Definition of generic fonts to use in the pages
SELECTED_FONT = ("Verdana 12 bold")
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)

# Gestion of the figure
f = Figure(facecolor="black")
a = f.add_subplot(111, facecolor="black")

# Set initial variables
current_cell = False
hide_membrane = False
cell_ves_nbr = 0
filename = ""
current_vesicle = False


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
            last_ves = vesicles[-1]
            last_pos = session.query(Position).\
                filter(Position.vesicle == last_ves).all()

            norm = mpl.colors.Normalize(vmin=0, vmax=last_pos[-1].t)
            ax = f.add_axes([0.9, 0.06, 0.02, 0.90], "Time frame")
            cb = mpl.colorbar.ColorbarBase(ax, cmap='magma', norm=norm,
                                           orientation="vertical")
            cb.set_label('Time frame')

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

                a.scatter(xpos, ypos, s=3, c=t, cmap='magma', norm=norm)

            if not hide_membrane:
                membrane = session.query(MembranePoint). \
                    filter(MembranePoint.cell == current_cell).all()
                for point in membrane:
                    x.append(point.x)
                    y.append(point.y)
                a.scatter(x, y, c='g', s=3)

            canvas.draw()

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

        label1 = ttk.Label(ves_selection, text="Select desired cell :")
        label1.grid(row=0, column=0)
        existingcells = session.query(Cell).all()
        cell_list = []
        for c in existingcells:
            cell_list.append(c.name)

        cmb = ttk.Combobox(ves_selection,
                           width="30",
                           values=cell_list,
                           state="readonly")
        cmb.bind("<<ComboboxSelected>>", lambda _: self.cell_change(cmb.get(),
                                                                    session))
        cmb.grid(row=0, column=1)
        vesLabel = ttk.Label(ves_selection, text="Select desired vesicle")
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
        choosenbr = ttk.Label(ves_selection, text="Choose a vesicle number")
        self.veschoice = tk.StringVar()
        vesnbr = ttk.Entry(ves_selection,  textvariable=self.veschoice)
        choosebtn = ttk.Button(ves_selection,
                               text="Go",
                               command=lambda: self.ves_update(
                                   session, vesnbr.get()),
                               style='my.TButton')
        vesLabel.grid(row=1, columnspan=2)
        prevButton.grid(row=2)
        nextButton.grid(row=2, column=1)
        choosenbr.grid(row=3)
        vesnbr.grid(row=3, column=1)
        choosebtn.grid(row=3, column=2)

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
        infoLabel = ttk.Label(infos, text='Vesicle informations')
        ilabel1 = ttk.Label(infos, text='Cell name :')
        ilabel2 = ttk.Label(infos, text='Vesicle number :')
        ilabel3 = ttk.Label(infos, text='Number of points :')
        ilabel4 = ttk.Label(infos, text='Behaviour before stimulation :')
        ilabel5 = ttk.Label(infos, text='Behaviour before stimulation :')
        info1 = ttk.Label(infos, textvariable=self.cell_value)
        info2 = ttk.Label(infos, textvariable=self.ves_value)
        info3 = ttk.Label(infos, textvariable=self.points_value)
        info4 = ttk.Label(infos, textvariable=self.bef_value)
        info5 = ttk.Label(infos, textvariable=self.aft_value)
        infoLabel.grid(row=0, columnspan=2)
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
        ves = \
        session.query(Vesicle).filter(Vesicle.cell == current_cell).all()[
            current_vesicle]

        # Update the first plot, vesicle traj
        self.trajplot.clear()
        xpos = []
        ypos = []
        t = []
        positions = session.query(Position). \
            filter(Position.vesicle == ves).all()
        for position in positions:
            xpos.append(position.x)
            ypos.append(position.y)
            t.append(position.t)

        self.trajplot.scatter(xpos, ypos, s=3, c=t, cmap='magma')
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

        self.msdaftcanv.draw()

        # Update the right panel values
        self.cell_value.set(current_cell.name)
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

        self.rowconfigure(0, minsize=50, weight=1)
        self.rowconfigure(1, minsize=150, weight=3)
        self.rowconfigure(2, minsize=250, weight=3)
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
        self.all_cells = tk.StringVar()

        # Subframe summarising what is displayed
        summary = tk.Frame(self, borderwidth=5, relief=tk.SUNKEN)
        slabel1 = ttk.Label(summary, text='Statistics displayed :')
        info1 = ttk.Label(summary, textvariable=self.stat_type)
        slabel2 = ttk.Label(summary, text='Type of stimulation :')
        info2 = ttk.Label(summary, textvariable=self.stimu_type)
        slabel3 = ttk.Label(summary, text='All cells included :')
        info3 = ttk.Label(summary, textvariable=self.all_cells)
        exportbutton = ttk.Button(summary, text='Export graph')
        slabel1.grid()
        slabel2.grid(row=1)
        slabel3.grid(row=2)
        info1.grid(column=1)
        info2.grid(row=1, column=1)
        info3.grid(row=2, column=1)
        exportbutton.grid(row=3, columnspan=2)
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
        type_label.grid(row=0)
        cmb.grid(row=0, column=1)
        selectcells = ttk.Button(stats_options,
                                 text="Chose cells to remove",
                                 command=lambda: popupmsg(
                                     "Not supported yet!"))
        remove = ttk.Checkbutton(stats_options, text="Remove selected cells")
        selectcells.grid(row=1)
        remove.grid(row=1, column=1)
        behav = session.query(BehaviourType).all()
        behav_list = []
        for b in behav:
            behav_list.append(b.type)
        original = ttk.Combobox(stats_options,
                                width="30",
                                values=behav_list,
                                state="readonly")
        original.bind("<<ComboboxSelected>>")
        original.grid(row=2)
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
        self.statsfig.clear()
        self.popsplot = self.statsfig.add_subplot(111)
        (fb, db, cb, fa, da, ca) = behavchange(session, stimu)

        # data
        n_groups = 3
        before = (fb, db, cb)
        after = (fa, da, ca)

        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.8

        self.popsplot.bar(index, before, bar_width, alpha=opacity,
                          color='b', label='Before')
        self.popsplot.bar(index + bar_width, after, bar_width,
                          alpha=opacity, color='g', label='After')
        self.popsplot.axes.set_xticklabels(('', 'Free', '',
                                            'Directed', '', 'Caged'))

        self.statcanvas.draw()

    def ch_vs_ori_display(self, session, stimu, original):
        self.statsfig.clear()
        self.popsplot = self.statsfig.add_subplot(111)
        (newfree, newdir, newcaged, calc) = chvsori(session, stimu, original)
        if calc:
            sum = len(newfree) + len(newdir) + len(newcaged)
            nfper = len(newfree) / sum
            ndper = len(newdir) / sum
            ncper = len(newcaged) / sum
        else:
            nfper = 0
            ndper = 0
            ncper = 0

        labels = ("Free", "Directed", "Caged")
        y_pos = np.arange(len(labels))
        values = [nfper, ndper, ncper]
        self.popsplot.bar(y_pos, values, align='center')
        labels = ("", "", "Free", "", "Directed", "", "Caged")
        self.popsplot.axes.set_xticklabels(labels, fontdict=None, minor=False)

        self.statcanvas.draw()

    def nine_quadrants_display(self, session, stimu):
        self.statsfig.clear()
        bins = np.linspace(0, 5, 11)

        # Originally free
        (newfree, newdir, newcaged, calc) = chvsori(session, stimu, "Free")

        self.ffsplot = self.statsfig.add_subplot(331)
        distances = dats(session, newfree)
        self.ffsplot.hist(distances, bins)
        self.fdsplot = self.statsfig.add_subplot(332)
        distances = dats(session, newdir)
        self.fdsplot.hist(distances, bins)
        self.fcsplot = self.statsfig.add_subplot(333)
        distances = dats(session, newcaged)
        self.fcsplot.hist(distances, bins)

        # Originally directed
        (newfree, newdir, newcaged, calc) = chvsori(session, stimu, "Directed")
        self.dfsplot = self.statsfig.add_subplot(334)
        distances = dats(session, newfree)
        self.dfsplot.hist(distances, bins)
        self.ddsplot = self.statsfig.add_subplot(335)
        distances = dats(session, newdir)
        self.ddsplot.hist(distances, bins)
        self.dcsplot = self.statsfig.add_subplot(336)
        distances = dats(session, newcaged)
        self.dcsplot.hist(distances, bins)

        # Originally caged
        (newfree, newdir, newcaged, calc) = chvsori(session, stimu, "Caged")
        self.cfsplot = self.statsfig.add_subplot(337)
        distances = dats(session, newfree)
        self.cfsplot.hist(distances, bins)
        self.cdsplot = self.statsfig.add_subplot(338)
        distances = dats(session, newdir)
        self.cdsplot.hist(distances, bins)
        self.ccsplot = self.statsfig.add_subplot(339)
        distances = dats(session, newcaged)
        self.ccsplot.hist(distances, bins)

        self.statcanvas.draw()
