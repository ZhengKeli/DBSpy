import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from spector.app.base import BaseController


class Controller(BaseController):
    def __init__(self, app, index):
        super().__init__(app)
        self.index = index
        self.process = app.process.spectrum_process_list[index].raw_process
        
        # conf var
        self.file_path_var = tk.StringVar()
        
        # conf
        conf_frame = tk.LabelFrame(self.frame, text='Raw data Configuration')
        conf_frame.grid(row=0, column=0, sticky='nesw')
        tk.Label(conf_frame, text='File path:').pack(anchor='w')
        tk.Entry(conf_frame, textvariable=self.file_path_var).pack(anchor='w', fill='both')
        self.reset()
        
        # apply & reset
        apply_frame = tk.Frame(self.frame)
        apply_frame.grid(row=1, column=0, sticky='ew')
        tk.Button(apply_frame, text='Apply', command=self.apply).pack(side='left')
        tk.Button(apply_frame, text='Reset').pack(side='left')
        
        # result
        result_frame = tk.LabelFrame(self.frame, text='Raw spectrum:')
        result_frame.grid(row=2, column=0, sticky='nesw')
        raw_spectrum = self.process.result
        if raw_spectrum is None:
            tk.Label(result_frame, text='Error').pack()
        else:
            figure, axis = plt.subplots()
            axis.plot(raw_spectrum.x, raw_spectrum.y)
            canvas = FigureCanvasTkAgg(figure, result_frame)
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, result_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(anchor='w', fill='both')
    
    def reset(self):
        file_path_value = self.process.conf.file_path
        if file_path_value is None:
            file_path_value = ''
        self.file_path_var.set(file_path_value)
    
    def apply(self):
        self.process.conf.file_path = self.file_path_var.get()
        self.app.process.try_process()
        self.app.update_frame(['spectrum', self.index, 'raw'])
