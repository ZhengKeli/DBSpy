import tkinter as tk
from tkinter import ttk

import spector.core as core
from .MainController import MainFrameController


class SpectorApp:
    def __init__(self, process: core.main.Process = None):
        if process is not None:
            self.process = process
        else:
            self.process = core.main.Process()
        
        self.window = tk.Tk("Spector")
        
        self.menu = None
        self.init_menu()
        
        self.tree: ttk.Treeview = None
        self.init_tree()
        
        self.controller = None
        self.init_frame()
        
        self.window.mainloop()
    
    def init_menu(self):
        self.menu = tk.Menu(self.window)
        menu_file = tk.Menu(self.menu, tearoff=0)
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open')
        self.menu.add_cascade(label="File", menu=menu_file)
        self.window.config(menu=self.menu)
        self.update_menu()
    
    def update_menu(self):
        pass
    
    def init_tree(self):
        self.tree = ttk.Treeview(self.window, show="tree")
        self.tree.pack(side='left', fill='y')
        self.tree.bind('<ButtonRelease-1>', self.on_tree_clicked)
        self.update_tree()
    
    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        main = self.tree.insert('', 'end', text='Main', value=['main'])
        for i, spectrum_process in enumerate(self.process.spectrum_process_list):
            self.tree.insert(main, 'end', text='Spectrum_' + str(i), value=['spectrum', i])
        for i, artifact_process in enumerate(self.process.artifact_process_list):
            self.tree.insert(main, 'end', text='Artifacts_' + str(i), value=['artifact', i])
    
    def on_tree_clicked(self, _):
        item = self.tree.item(self.tree.focus())
        values = item['values']
        if len(values) > 0:
            self.update_frame(values)
    
    def init_frame(self):
        self.update_frame(['main'])
    
    def update_frame(self, key=None):
        if self.controller is not None:
            self.controller.frame.destroy()
        
        if key is None or len(key) == 0:
            self.controller = None
            return
    
        if key[0] == 'main':
            self.controller = MainFrameController(self)
            self.controller.frame.pack(side='left', fill='both')
        elif key[0] == 'spectrum':
            pass
        elif key[0] == 'artifact':
            pass