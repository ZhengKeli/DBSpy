import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from dbspy.core.spectrum.cdbs.raw import Conf
from dbspy.gui import base


class Controller(base.ElementProcessController):
    def __init__(self, app, index):
        self.index = index
        self.conf_file_path = tk.StringVar()
        self.result_figure: plt.Figure = plt.figure(figsize=(5, 5))
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
        axe = self.result_figure.gca()
        if result is not None:
            (xi, xj), y = result
            smy = ndi.gaussian_filter(np.log(y + 1), 3.0)
            axe.imshow(smy, extent=[xj[0], xj[-1], xi[-1], xi[0]], cmap='Greys')
            axe.contour(xj, xi, smy, colors='k')
        else:
            axe.set_title("Error!")
            # todo show info
        self.result_figure.tight_layout()
        self.result_figure.canvas.draw()
        self.result_figure.canvas.flush_events()
