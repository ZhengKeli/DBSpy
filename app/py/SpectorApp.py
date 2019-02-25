import tkinter as tk
from tkinter import ttk


class SpectorApp:
    def __init__(self, spector=None):
        self.spector = spector
        self.window = tk.Tk("Spector")
        
        menu = tk.Menu(self.window)
        menu_file = tk.Menu(menu, tearoff=0)
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open')
        menu.add_cascade(label="File", menu=menu_file)
        self.window.config(menu=menu)
        
        self.tree = ttk.Treeview(self.window, show="tree")
        self.tree.grid(column=0)
    
    def update(self):
        pass
