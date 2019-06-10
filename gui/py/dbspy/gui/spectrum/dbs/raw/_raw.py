import tkinter as tk

import matplotlib.pyplot as plt

from dbspy.core.spectrum.dbs.raw import Conf
from dbspy.gui import base


class Controller(base.FigureResultController, base.ElementProcessController):
    def __init__(self, app, index):
        self.index = index
        self.conf_file_path = tk.StringVar()
        super().__init__(
            app.container,
            app.process.spectrum_processes[index].raw_process,
            plt.figure(figsize=(6, 3)))
    
    def on_create_info_frame(self, info_frame):
        tk.Label(info_frame, text='Raw Data').pack()
    
    def on_create_conf_frame(self, conf_frame):
        tk.Label(conf_frame, text='File path:').pack(anchor='w')
        tk.Entry(conf_frame, textvariable=self.conf_file_path).pack(anchor='w', fill='both')
    
    def on_reset(self, conf: Conf):
        self.conf_file_path.set(str(conf.file_path))
    
    def on_apply(self) -> Conf:
        return Conf(self.conf_file_path.get())
    
    def on_update_draw(self, figure, result, exception):
        axe = figure.gca()
        if result is not None:
            x, y = result
            axe.plot(x, y)
        else:
            axe.set_title("Error!")
            # todo show info
