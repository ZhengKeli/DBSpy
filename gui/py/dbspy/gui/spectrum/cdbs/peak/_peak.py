import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndi

from dbspy.core.spectrum.cdbs.peak import Conf
from dbspy.core.utils.neighborhood import neighborhood
from dbspy.gui import base
from dbspy.gui.utils.figure import FigureResultController


class Controller(FigureResultController, base.ElementProcessController):
    def __init__(self, app, index):
        self.conf_mean_center = tk.StringVar()
        self.conf_mean_radius = tk.StringVar()
        self.conf_diff_center = tk.StringVar()
        self.conf_diff_radius = tk.StringVar()
        super().__init__(
            app.container,
            app.process.spectrum_processes[index].peak_process,
            plt.figure(figsize=(5, 5)))
    
    def on_create_info_frame(self, info_frame):
        tk.Label(info_frame, text='Peak').pack()
    
    def on_create_conf_frame(self, conf_frame):
        tk.Label(conf_frame, text='mean_center=').pack(side='left')
        tk.Entry(conf_frame, width=6, textvariable=self.conf_mean_center).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
        
        tk.Label(conf_frame, text='mean_radius=').pack(side='left', padx=(10, 0))
        tk.Entry(conf_frame, width=6, textvariable=self.conf_mean_radius).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
        
        tk.Label(conf_frame, text='diff_center=').pack(side='left')
        tk.Entry(conf_frame, width=6, textvariable=self.conf_diff_center).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
        
        tk.Label(conf_frame, text='diff_radius=').pack(side='left', padx=(10, 0))
        tk.Entry(conf_frame, width=6, textvariable=self.conf_diff_radius).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
    
    def on_reset(self, conf: Conf):
        self.conf_mean_center.set(str(np.mean(conf.search_range_xm)))
        self.conf_mean_radius.set(str(conf.peak_radius_xm))
        self.conf_diff_center.set(str(np.mean(conf.search_range_xd)))
        self.conf_diff_radius.set(str(conf.peak_radius_xd))
    
    def on_apply(self) -> Conf:
        mean_center = float(self.conf_mean_center.get())
        mean_radius = float(self.conf_mean_radius.get())
        diff_center = float(self.conf_diff_center.get())
        diff_radius = float(self.conf_diff_radius.get())
        return Conf(
            search_range_xm=neighborhood(mean_center, mean_radius / 2),
            peak_radius_xm=mean_radius,
            search_range_xd=neighborhood(diff_center, diff_radius / 2),
            peak_radius_xd=diff_radius)
    
    def on_update_draw(self, figure, result, exception):
        axe = figure.gca()
        if result is not None:
            _, ((xd, xm), y, _), (peak_id, peak_im) = result
            peak_xd = xd[peak_id]
            peak_xm = xm[peak_im]
            
            smy = ndi.gaussian_filter(np.log(y + 1), 3.0)
            axe.imshow(smy, extent=[xm[0], xm[-1], xd[-1], xd[0]], cmap='Greys')
            axe.contour(xm, xd, smy, colors='k')
            axe.set_xlabel("(Ea+Eb)/2, eV")
            axe.set_ylabel("(Ea-Eb)/2, eV")
            axe.plot([peak_xm, peak_xm], [xd[-1], xd[0]], '--', color='black')
            axe.plot([xm[0], xm[-1]], [peak_xd, peak_xd], '--', color='black')
        else:
            axe.set_title("Error!")
            # todo show info
