import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from dbspy.app.base import BaseController


class Controller(BaseController):
    def __init__(self, app, index):
        super().__init__(app)
        self.index = index
        self.process = app.process.spectrum_processes[index].raw_process
        
        # conf
        self.conf_file_path = tk.StringVar()
        
        conf_frame = tk.LabelFrame(self.frame, text='Configuration')
        conf_frame.grid(row=0, column=0, sticky='nesw')
        tk.Label(conf_frame, text='File path:').pack(anchor='w')
        tk.Entry(conf_frame, textvariable=self.conf_file_path).pack(anchor='w', fill='both')
        
        self.reset()
        
        # operation
        apply_frame = tk.Frame(self.frame)
        apply_frame.grid(row=1, column=0, sticky='ew')
        tk.Button(apply_frame, text='Apply', command=self.apply).pack(side='left')
        tk.Button(apply_frame, text='Reset', command=self.reset).pack(side='left')
        
        # result
        result_frame = tk.LabelFrame(self.frame, text='Result:')
        result_frame.grid(row=2, column=0, sticky='nesw')
        
        self.result_state = tk.StringVar()
        tk.Label(result_frame, textvariable=self.result_state).pack(anchor='w', fill='both')
        
        self.result_figure: plt.Figure = plt.figure(figsize=(5, 3))
        canvas = FigureCanvasTkAgg(self.result_figure, result_frame)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, result_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(anchor='w', fill='both')
        
        self.update()
    
    def reset(self):
        file_path_value = self.process.conf.file_path
        if file_path_value is None:
            file_path_value = ''
        self.conf_file_path.set(file_path_value)
    
    def apply(self):
        self.process.conf.file_path = self.conf_file_path.get()
        self.app.process.try_process()
        self.update()
    
    def update(self):
        self.result_figure.clear()
        try:
            x, y = self.process.value
            self.result_figure.gca().plot(x, y)
        except Exception:
            self.result_state.set("Error!")
            # todo show info
        self.result_figure.tight_layout()
        self.result_figure.canvas.draw()
        self.result_figure.canvas.flush_events()
