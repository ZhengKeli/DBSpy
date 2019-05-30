import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from dbspy.app import base
from dbspy.core.spectrum.dbs.raw import Conf


class Controller(base.ElementProcessController):
    def __init__(self, app, index):
        self.index = index
        self.conf_file_path = tk.StringVar()
        self.result_figure: plt.Figure = plt.figure(figsize=(5, 3))
        super().__init__(app.container, app.process.spectrum_processes[index].raw_process)
    
    def on_create_info_frame(self, info_frame):
        tk.Label(info_frame, text='Raw Data').pack()
    
    def on_create_conf_frame(self, conf_frame):
        tk.Label(conf_frame, text='File path:').pack(anchor='w')
        tk.Entry(conf_frame, textvariable=self.conf_file_path).pack(anchor='w', fill='both')
    
    def on_create_result_frame(self, result_frame):
        canvas = FigureCanvasTkAgg(self.result_figure, result_frame)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, result_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()
    
    def on_reset(self, conf: Conf):
        self.conf_file_path.set(str(conf.file_path))
    
    def on_apply(self) -> Conf:
        return Conf(self.conf_file_path.get())
    
    def on_update(self, result, exception=None):
        self.result_figure.clear()
        if result is not None:
            x, y = result
            self.result_figure.gca().plot(x, y)
        else:
            self.result_figure.gca().set_title("Error!")
            # todo show info
        self.result_figure.tight_layout()
        self.result_figure.canvas.draw()
        self.result_figure.canvas.flush_events()
