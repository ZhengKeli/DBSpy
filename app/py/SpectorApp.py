import tkinter as tk
from tkinter import ttk

import spector
from SpectorFrameController import SpectorFrameController


class SpectorApp:
    def __init__(self, spector_process: spector.Process):
        self.spector_process = spector_process
        self.window = tk.Tk("Spector")
        
        self.menu = None
        self.init_menu()
        self.update_menu()
        
        self.tree: ttk.Treeview = None
        self.init_tree()
        self.update_tree()
        
        self.frame_controller = None
        self.init_frame()
        self.update_frame()
        
        self.window.mainloop()
    
    def init_menu(self):
        self.menu = tk.Menu(self.window)
        menu_file = tk.Menu(self.menu, tearoff=0)
        menu_file.add_command(label='New', )
        menu_file.add_command(label='Open')
        self.menu.add_cascade(label="File", menu=menu_file)
        self.window.config(menu=self.menu)
    
    def update_menu(self):
        pass
    
    def init_tree(self):
        self.tree = ttk.Treeview(self.window, show="tree")
        self.tree.pack(side='left', fill='y')

        self.tree.bind('<ButtonRelease-1>', self.on_tree_clicked)
    
    def on_tree_clicked(self, event):
        item = self.tree.item(self.tree.focus())
        values = item['values']
        if len(values) > 0:
            self.update_frame(values)
    
    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        spectrum_tree = self.tree.insert('', 0, text='Spectrums', value='spector')
        for i, spectrum_process in enumerate(self.spector_process.spectrum_process_list):
            self.tree.insert(spectrum_tree, 0, text='Spectrum_' + str(i), value=['spectrum', i])
        
        artifact_tree = self.tree.insert('', 0, value='spector', text='Artifacts')
        for i, artifact_process in enumerate(self.spector_process.artifact_process_list):
            self.tree.insert(artifact_tree, 1, text='Artifacts_' + str(i), value=['artifact', i])
    
    def init_frame(self):
        pass
    
    def update_frame(self, key=None):
        if self.frame_controller is not None:
            self.frame_controller.frame.destroy()
        
        if key is None or len(key) == 0:
            self.frame_controller = None
            return
        
        if key[0] == 'spector':
            self.frame_controller = SpectorFrameController(self)
            self.frame_controller.frame.pack(side='left', fill='both')
        elif key[0] == 'spectrum':
            pass
        elif key[0] == 'artifact':
            pass
