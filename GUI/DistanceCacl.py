import tkinter as tk
from tkinter import ttk

from Models import Cell, Vesicle, Position
from .PopupMsg import popupmsg
from Calculation.DistanceFromMembrane import massDistanceFromMembrane


def distance_dialog(session):
    dialog = tk.Toplevel()
    dialog.minsize(400, 300)
    dialog.wm_title("Calculate distance between vesicles and the membrane")
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
                          command=lambda: calculate_distance(dialog,
                                                             session,
                                                             cellchoice.get()))
    validate.grid(row=1, columnspan=2)


def calculate_distance(dialog, session, name):
    cell = session.query(Cell).filter(Cell.name == name).first()

    first_ves = session.query(Vesicle).filter(Vesicle.cell == cell).first()
    firstdist = session.query(Position)\
        .filter(Position.vesicle == first_ves).first().distance

    if not firstdist:
        massDistanceFromMembrane(session, cell)
        dialog.destroy()

    else:
        popupmsg("This cell's distances from membrane "
                 "have already been calculated.")
