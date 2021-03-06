import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np

from dbspy.gui import base
from dbspy.gui.utils.figure import FigureResultController
from dbspy.core.spectrum import dbs
from dbspy.core.spectrum.dbs.peak import Conf
from dbspy.core.utils.neighborhood import neighborhood


class Controller(FigureResultController, base.ElementProcessController):
    def __init__(self, app, index):
        self.spectrum_process: dbs.Process = app.process.spectrum_processes[index]
        self.index = index
        self.conf_center = tk.StringVar()
        self.conf_radius = tk.StringVar()
        super().__init__(
            app.container,
            self.spectrum_process.peak_process,
            plt.figure(figsize=(6, 3)))

    def on_create_info_frame(self, info_frame):
        tk.Label(info_frame, text='Peak').pack()

    def on_create_conf_frame(self, conf_frame):
        tk.Label(conf_frame, text='center=').pack(side='left')
        tk.Entry(conf_frame, width=6, textvariable=self.conf_center).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')

        tk.Label(conf_frame, text='radius=').pack(side='left', padx=(10, 0))
        tk.Entry(conf_frame, width=6, textvariable=self.conf_radius).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')

    def on_reset(self, conf: Conf):
        self.conf_center.set(str(np.mean(conf.search_range)))
        self.conf_radius.set(str(conf.peak_radius))

    def on_apply(self) -> Conf:
        center = float(self.conf_center.get())
        radius = float(self.conf_radius.get())
        return Conf(
            search_range=neighborhood(center, radius / 2),
            peak_radius=radius)

    def on_update_draw(self, figure, result, exception):
        axe = figure.gca()
        if result is not None:
            _, (peak_x, peak_y, _), peak_center_i = result
            raw_x, raw_y = self.spectrum_process.raw_process.value
            peak_center = peak_x[peak_center_i]

            axe.semilogy(raw_x, raw_y)
            axe.semilogy(peak_x, peak_y)
            axe.semilogy((peak_center, peak_center), (0, 1.3 * np.max(peak_y)), '--', color='black')
        else:
            axe.set_title("Error!")
            # todo show info
