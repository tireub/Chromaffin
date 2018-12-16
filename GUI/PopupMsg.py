import tkinter as tk
from tkinter import ttk


NORM_FONT = ("Verdana", 10)

# Definition of a simple popup message that closes itself with a button
# Input is the message to display
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Warning !")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="OK", command=popup.destroy)
    B1.pack()
    popup.mainloop()