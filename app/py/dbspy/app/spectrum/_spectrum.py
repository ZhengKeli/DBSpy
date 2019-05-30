import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from dbspy.app import base


class Controller(base.ProcessController):
    def __init__(self, app, index):
        self.app = app
        self.index = index
        self.result_figure: plt.Figure = plt.figure()
        super().__init__(app.container, app.process.spectrum_processes[index])
    
    def on_create_info_frame(self, info_frame):
        tk.Label(info_frame, text='DBS Spectrum (tag=' + str(self.process.tag) + ')').pack()
        tk.Button(info_frame, text='Remove', foreground='red', command=self.remove).pack()
    
    def on_create_result_frame(self, result_frame):
        canvas = FigureCanvasTkAgg(self.result_figure, result_frame)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, result_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(anchor='w', fill='both')
    
    def on_update(self, result, exception):
        self.result_figure.clear()
        if result is not None:
            (x, y, _), _ = self.process.value
            self.result_figure.gca().semilogy(x, y)
        else:
            self.result_figure.gca().set_title("Error!")
            # todo show info
        self.result_figure.tight_layout()
        self.result_figure.canvas.draw()
        self.result_figure.canvas.flush_events()
    
    def remove(self):
        self.app.process.remove_spectrum_process(self.process)
        self.app.update_frame(['main'])
        self.app.update_tree()
