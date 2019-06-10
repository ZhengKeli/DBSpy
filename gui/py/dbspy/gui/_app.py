import tkinter as tk
from tkinter import ttk
from typing import Optional

import dbspy.core as core
from dbspy.gui import main
from . import spectrum, analyze, base


class Application:
    def __init__(self, process: core.Process = None):
        self.process: core.Process = core.Process() if process is None else process
        
        self.window = tk.Tk()
        self.window.title("DBSpy")
        
        self.menu = None
        self.key = None
        self.init_menu()
        
        self.tree = None
        self.init_tree()
        
        self.container = tk.Frame(self.window, width=500, height=500)
        self.container.pack(side='left', fill='both', padx='4p', pady='4p')
        self.controller: Optional[base.WidgetController] = None
        self.init_frame()
        
        self.window.mainloop()
    
    def init_menu(self):
        self.menu = tk.Menu(self.window)
        
        menu_file = tk.Menu(self.menu, tearoff=0)
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open')
        self.menu.add_cascade(label="File", menu=menu_file)
        
        menu_help = tk.Menu(self.menu, tearoff=0)
        menu_help.add_command(label='About')
        self.menu.add_cascade(label='Help', menu=menu_help)
        
        self.window.config(menu=self.menu)
        self.update_menu()
    
    def update_menu(self):
        pass
    
    def init_tree(self):
        self.tree: ttk.Treeview = ttk.Treeview(self.window, show="tree")
        self.tree.pack(side='left', fill='y')
        self.tree.bind('<ButtonRelease-1>', self.on_tree_clicked)
        self.update_tree()
    
    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        main_node = self.tree.insert('', 'end', text='Main', value=['main'], open=True)
        
        for i, spectrum_process in enumerate(self.process.spectrum_processes):
            tag = str(spectrum_process.tag)
            if isinstance(spectrum_process, core.spectrum.dbs.Process):
                spectrum_node = self.tree.insert(main_node, 'end', text='DBS Spectrum ' + tag, value=['spectrum', i])
                self.tree.insert(spectrum_node, 'end', text='raw', value=['spectrum', i, 'raw'])
                self.tree.insert(spectrum_node, 'end', text='res', value=['spectrum', i, 'res'])
                self.tree.insert(spectrum_node, 'end', text='peak', value=['spectrum', i, 'peak'])
                self.tree.insert(spectrum_node, 'end', text='bg', value=['spectrum', i, 'bg'])
            elif isinstance(spectrum_process, core.spectrum.cdbs.Process):
                spectrum_node = self.tree.insert(main_node, 'end', text='CDBS Spectrum ' + tag, value=['spectrum', i])
                self.tree.insert(spectrum_node, 'end', text='raw', value=['spectrum', i, 'raw'])
                self.tree.insert(spectrum_node, 'end', text='peak', value=['spectrum', i, 'peak'])
                self.tree.insert(spectrum_node, 'end', text='sp', value=['spectrum', i, 'bg'])
        
        for i, analyze_process in enumerate(self.process.analyze_processes):
            if isinstance(analyze_process, core.analyze.sw.Process):
                self.tree.insert(main_node, 'end', text='SW Analyze', value=['analyze', i])
            elif isinstance(analyze_process, core.analyze.curve.Process):
                self.tree.insert(main_node, 'end', text='Curve Analyze', value=['analyze', i])
    
    def on_tree_clicked(self, _):
        item = self.tree.item(self.tree.focus())
        values = item['values']
        if len(values) > 0:
            self.update_frame(values)
    
    def init_frame(self):
        self.update_frame(['main'])
    
    def update_frame(self, key=None):
        if self.key == key:
            return
        
        self.controller = None
        for child in self.container.winfo_children():
            child.destroy()
        
        if key is None or len(key) == 0:
            tk.Label(self.container, text="Nothing to show").pack()
        elif key[0] == 'main':
            self.controller = main.Controller(self)
        elif key[0] == 'spectrum':
            spectrum_index = key[1]
            spectrum_process = self.process.spectrum_processes[spectrum_index]
            if len(key) == 2:
                self.controller = spectrum.Controller(self, spectrum_index)
            elif isinstance(spectrum_process, core.spectrum.dbs.Process):
                if key[2] == 'raw':
                    self.controller = spectrum.dbs.raw.Controller(self, spectrum_index)
                elif key[2] == 'res':
                    self.controller = spectrum.dbs.res.Controller(self, spectrum_index)
                elif key[2] == 'peak':
                    self.controller = spectrum.dbs.peak.Controller(self, spectrum_index)
                elif key[2] == 'bg':
                    self.controller = spectrum.dbs.bg.Controller(self, spectrum_index)
            elif isinstance(spectrum_process, core.spectrum.cdbs.Process):
                if key[2] == 'raw':
                    self.controller = spectrum.cdbs.raw.Controller(self, spectrum_index)
                elif key[2] == 'peak':
                    self.controller = spectrum.cdbs.peak.Controller(self, spectrum_index)
                elif key[2] == 'sp':
                    pass  # todo sub items
        elif key[0] == 'analyze':
            analyze_index = key[1]
            analyze_process = self.process.analyze_processes[analyze_index]
            if isinstance(analyze_process, core.analyze.sw.Process):
                self.controller = analyze.sw.Controller(self, analyze_index)
            elif isinstance(analyze_process, core.analyze.curve.Process):
                self.controller = analyze.curve.Controller(self, analyze_index)
        if self.controller is not None:
            self.controller.widget.pack(fill='both')
        self.key = key
