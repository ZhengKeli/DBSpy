import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from spector.app.base import BaseController
from spector.utils.spectrum import Spectrum


class Controller(BaseController):
    def __init__(self, app, index):
        super().__init__(app)
        self.index = index
        self.process = app.process.spectrum_process_list[index].raw_process
        
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
        self.result_state = tk.StringVar()
        self.result_figure: plt.Figure = plt.figure()

        result_frame = tk.LabelFrame(self.frame, text='Result:')
        result_frame.grid(row=2, column=0, sticky='nesw')
        tk.Label(result_frame, textvariable=self.result_state).pack(anchor='w', fill='both')
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
        self.update()

    def update(self):
        self.app.process.try_process()
        raw_spectrum = self.process.result

        self.result_figure.clear()
        if isinstance(raw_spectrum, Spectrum):
            self.result_state.set("State:Success")
            self.result_figure.gca().plot(raw_spectrum.x, raw_spectrum.y)
        else:
            self.result_state.set("State:Error")
            # todo show info
        self.result_figure.canvas.draw()
        self.result_figure.canvas.flush_events()
