import tkinter as tk
from tkinter import ttk

from Models import Cell, Vesicle, MSD
from Calculation.MSDCalc import CellMSDs
from Calculation.BehaviourSorting import cellSorting
from .PopupMsg import popupmsg


def MSD_dialog(session):
    dialog = tk.Toplevel()
    dialog.minsize(400, 300)
    dialog.wm_title("Calculate MSDs and sort vesicles")
    label = ttk.Label(dialog, text="Select cell:")

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

    validate = ttk.Button(dialog,
                          text="Import",
                          command=lambda: calculateMSD(dialog,
                                                       session,
                                                       cellchoice.get()))
    validate.grid(row=1, columnspan=2)


def calculateMSD(dialog, session, name):
    cell = session.query(Cell).filter(Cell.name == name).first()

    first_ves = session.query(Vesicle).filter(Vesicle.cell == cell).first()
    firstMSD = session.query(MSD).filter(MSD.vesicle == first_ves).first()
    print(firstMSD)
    if not firstMSD:
        CellMSDs(session, cell)
        cellSorting(session, cell)
        dialog.destroy()

    else:
        popupmsg("This cell's MSDs have already been calculated.")

