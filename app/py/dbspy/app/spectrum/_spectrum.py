import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from dbspy.app.base import BaseController


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
        self.result_figure.clear()
        try:
            (x, y, _), _ = self.process.value
            self.result_figure.gca().semilogy(x, y)
            self.result_state.set("State:Success")
        except Exception as e:
            print(e)
            self.result_state.set("State:Error")
            # todo show info
        self.result_figure.canvas.draw()
        self.result_figure.canvas.flush_events()
    
    def on_remove(self):
        self.app.process.remove_spectrum_process(self.process)
        self.app.update_frame(['main'])
        self.app.update_tree()
