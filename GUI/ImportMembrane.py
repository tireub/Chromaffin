import tkinter as tk
from tkinter import ttk

from Models import Cell, MembranePoint
from .NewCell import browse_file
from Imports.Imports import edges_import
from .PopupMsg import popupmsg
from Calculation.DistanceFromMembrane import massDistanceFromMembrane


def membrane_dialog(session):
    dialog = tk.Toplevel()
    dialog.minsize(300, 200)
    for i in range(4):
        dialog.rowconfigure(i, weight=1)
    dialog.wm_title("Import membrane positions")
    label = ttk.Label(dialog, text="Select associated cell:")

    cells = session.query(Cell).all()
    celllist = []
    for cell in cells:
        celllist.append(cell.name)

    cellchoice = ttk.Combobox(dialog,
                              width="30",
                              values=celllist,
                              state="readonly")

    label.grid(row=0)
    cellchoice.grid(row=0, column=1)

    fileloc = tk.Frame(dialog)
    label2 = ttk.Label(fileloc, text="Choose file location:")
    txt = ttk.Entry(fileloc, width=50)
    browse = ttk.Button(fileloc, text="Browse",
                        command=lambda: browse_file(txt))
    label2.grid(row=0)
    txt.grid(row=1)
    browse.grid(row=1, column=1)
    fileloc.grid(row=1, columnspan=2)

    option = tk.Frame(dialog)
    label4 = ttk.Label(option, text="Calculate distances from membrane ?")
    calc = tk.BooleanVar()
    chkbx = tk.Checkbutton(option, variable=calc)
    label4.grid()
    chkbx.grid(row=0, column=1)
    option.grid(row=2, columnspan=2)

    validate = ttk.Button(dialog,
                          text="Import",
                          command=lambda: import_membrane(dialog,
                                                          session,
                                                          cellchoice.get(),
                                                          txt.get(),
                                                          calc.get()))

    validate.grid(row=3, columnspan=2, sticky="NSEW")


def import_membrane(dialog, session, name, file, calc):
    cell = session.query(Cell).filter(Cell.name == name).first()
    firstpoint = session.query(MembranePoint).\
        filter(MembranePoint.cell == cell).first()

    # Check if the membrane points already exists
    if not firstpoint:
        edges_import(session, file, cell)
        # Automatic distances calculation option
        if calc:
            massDistanceFromMembrane(session, cell)

        dialog.destroy()

    # If there is some membrane points, raise error message
    else:
        popupmsg("This cell already has membrane data.")
