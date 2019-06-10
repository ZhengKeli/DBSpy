import tkinter as tk
from collections import Iterable

import matplotlib.pyplot as plt

from dbspy.core.spectrum import dbs
from dbspy.core.spectrum.dbs.bg import Conf
from dbspy.gui import base


class Controller(base.FigureResultController, base.ElementProcessController):
    def __init__(self, app, index):
        self.spectrum_process: dbs.Process = app.process.spectrum_processes[index]
        self.index = index
        self.conf_radius = tk.StringVar()
        self.conf_expand = tk.StringVar()
        super().__init__(
            app.container,
            self.spectrum_process.bg_process,
            plt.figure(figsize=(6, 3)))
    
    def on_create_info_frame(self, info_frame):
        tk.Label(info_frame, text='Background').pack()
    
    def on_create_conf_frame(self, conf_frame):
        tk.Label(conf_frame, text='radius=').pack(side='left')
        tk.Entry(conf_frame, textvariable=self.conf_radius, width=6).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
        
        tk.Label(conf_frame, text='expand=').pack(side='left', padx=(10, 0))
        tk.Entry(conf_frame, textvariable=self.conf_expand, width=6).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
    
    def on_reset(self, conf: Conf):
        self.conf_radius.set(str(conf.bg_radius))
        if isinstance(conf.bg_expand, Iterable):
            expand = '  '.join(str(item) for item in conf.bg_expand)
        else:
            expand = str(conf.bg_expand)
        self.conf_expand.set(expand)
    
    def on_apply(self) -> Conf:
        expand = self.conf_expand.get().split()
        if len(expand) == 1:
            expand = expand[0], expand[0]
        expand = tuple(float(item) for item in expand)
        return Conf(
            bg_radius=float(self.conf_radius.get()),
            bg_expand=expand)
    
    def on_draw_result(self, figure, result, exception):
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
