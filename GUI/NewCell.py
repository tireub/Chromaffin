import tkinter as tk
from tkinter import ttk, END, filedialog

from Models import StimulationType, Cell
from Imports.Imports import cell_import
from Calculation.BehaviourSorting import cellSorting
from Calculation.MSDCalc import CellMSDs

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


def browse_file(entrytofill):
    global filename

    filename = filedialog.askopenfilename()
    entrytofill.delete(0, END)
    entrytofill.insert(0, filename)