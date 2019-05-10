import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from dbs.app.base import BaseController
from dbs.utils.spectrum import Spectrum


class Controller(BaseController):
    def __init__(self, app, index):
        super().__init__(app)
        self.index = index
        self.process = app.process.spectrum_processes[index]
        
        # info
        tk.Label(self.frame, text='This is a DBS Spectrum').grid(row=0)

        # operation
        tk.Button(self.frame, text='Remove', foreground='red', command=self.on_remove).grid(row=1)

        # result
        self.result_state = tk.StringVar()
        self.result_figure: plt.Figure = plt.figure()

        result_frame = tk.LabelFrame(self.frame, text='Result:')
        result_frame.grid(row=2, sticky='nesw')
        tk.Label(result_frame, textvariable=self.result_state).pack(anchor='w', fill='both')
        canvas = FigureCanvasTkAgg(self.result_figure, result_frame)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, result_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(anchor='w', fill='both')

        self.update()

    def update(self):
        _, sp_spectrum, _ = self.process.value
        
        self.result_figure.clear()
        if isinstance(sp_spectrum, Spectrum):
            self.result_state.set("State:Success")
            self.result_figure.gca().semilogy(sp_spectrum.x, sp_spectrum.y)
        else:
            self.result_state.set("State:Error")
            # todo show info
    
        self.result_figure.canvas.draw()
        self.result_figure.canvas.flush_events()
    
    def on_remove(self):
        del self.app.process.spectrum_process_list[self.index]
        self.app.update_frame(['main'])
        self.app.update_tree()
