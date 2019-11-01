import sys
import tkinter as tk
from dbspy.gui.app import Application

args = sys.argv
app_path = args[0] if len(args) > 0 else None
conf_path = args[1] if len(args) > 1 else None

root = tk.Tk()
root.withdraw()
Application(root, app_path, conf_path)
root.mainloop()
