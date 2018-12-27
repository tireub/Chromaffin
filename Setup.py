import cx_Freeze
import sys
import os


os.environ['TCL_LIBRARY'] = "C:\\Users\\Guillaume\\AppData\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Guillaume\\AppData\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"
base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("app.py", base=base)]

cx_Freeze.setup(
    name = "Chromaffin",
    options = {"build_exe": {"packages": ["tkinter","matplotlib"]}},
    version = "0.01",
    description = "Chromaffin studies application",
    executables = executables
)

