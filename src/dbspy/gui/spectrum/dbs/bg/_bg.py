import tkinter as tk
from collections import Iterable

import matplotlib.pyplot as plt

from dbspy.gui import base
from dbspy.gui.spectrum import dbs
from dbspy.gui.utils.figure import FigureResultController
from dbspy.core.spectrum.dbs import Conf


class Controller(FigureResultController, base.ElementProcessController):
    def __init__(self, app, index):
        self.spectrum_process: dbs.Process = app.process.spectrum_processes[index]
        self.index = index
        self.conf_radius = tk.StringVar()
        self.conf_left_expand = tk.StringVar()
        self.conf_right_expand = tk.StringVar()
        super().__init__(
            app.container,
            self.spectrum_process.bg_process,
            plt.figure(figsize=(6, 3)))
    
    def on_create_info_frame(self, info_frame):
        tk.Label(info_frame, text='Background').pack()
    
    def on_create_conf_frame(self, conf_frame):
        tk.Label(conf_frame, text='radius=').pack(side='left')
        tk.Entry(conf_frame, width=6, textvariable=self.conf_radius).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
        
        tk.Label(conf_frame, text='left_expand=').pack(side='left', padx=(10, 0))
        tk.Entry(conf_frame, width=6, textvariable=self.conf_left_expand).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
        
        tk.Label(conf_frame, text='right_expand=').pack(side='left', padx=(10, 0))
        tk.Entry(conf_frame, width=6, textvariable=self.conf_right_expand).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
    
    def on_reset(self, conf: Conf):
        self.conf_radius.set(str(conf.bg_radius))
        
        if isinstance(conf.bg_expand, Iterable):
            left_expand, right_expand = conf.bg_expand
        else:
            left_expand = right_expand = conf.bg_expand
        self.conf_left_expand.set(str(left_expand))
        self.conf_right_expand.set(str(right_expand))
    
    def on_apply(self) -> Conf:
        left_expand = float(self.conf_left_expand.get())
        right_expand = float(self.conf_right_expand.get())
        return Conf(
            bg_radius=float(self.conf_radius.get()),
            bg_expand=(left_expand, right_expand))
    
    def on_update_draw(self, figure, result, exception):
        axe = figure.gca()
        if result is not None:
            _, (peak_x, peak_y, _), peak_center_i = self.spectrum_process.peak_process.value
            bg_range_i, (bg_x, bg_y) = result
            
            plt.semilogy(
                (peak_x[peak_center_i], peak_x[peak_center_i]),
                (0, 1.3 * peak_y[peak_center_i]), '--', color='black')
            axe.semilogy(peak_x, peak_y, label='raw')
            axe.semilogy(bg_x, bg_y, label='background')
        else:
            axe.set_title("Error!")
            # todo show info
