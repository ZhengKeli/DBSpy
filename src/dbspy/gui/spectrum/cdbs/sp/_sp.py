import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

from dbspy.gui import base
from dbspy.gui.utils.figure import FigureResultController
from dbspy.core.spectrum.cdbs import Conf
from dbspy.core.utils.neighborhood import neighborhood


class Controller(FigureResultController, base.ElementProcessController):
    def __init__(self, app, index):
        self.spectrum_process = app.process.spectrum_processes[index]
        self.conf_sp_band_radius = tk.StringVar()
        self.conf_res_band_radius = tk.StringVar()
        self.result_resolution = tk.StringVar()
        super().__init__(
            app.container,
            self.spectrum_process.sp_process,
            plt.figure(figsize=(9, 3)))
    
    def on_create_info_frame(self, info_frame):
        tk.Label(info_frame, text='Peak').pack()
    
    def on_create_conf_frame(self, conf_frame):
        tk.Label(conf_frame, text='sp_band_radius=').pack(side='left')
        tk.Entry(conf_frame, width=6, textvariable=self.conf_sp_band_radius).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
        
        tk.Label(conf_frame, text='res_band_radius=').pack(side='left', padx=(10, 0))
        tk.Entry(conf_frame, width=6, textvariable=self.conf_res_band_radius).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
    
    def on_create_result_frame(self, result_frame):
        tk.Label(result_frame, textvar=self.result_resolution).pack()
        super().on_create_result_frame(result_frame)
    
    def on_reset(self, conf: Conf):
        self.conf_sp_band_radius.set(str(conf.sp_band_radius))
        self.conf_res_band_radius.set(str(conf.res_band_radius))
    
    def on_apply(self) -> Conf:
        return Conf(
            sp_band_radius=float(self.conf_sp_band_radius.get()),
            res_band_radius=float(self.conf_res_band_radius.get()))
    
    def on_update(self, result, exception):
        if result is not None:
            _, (resolution, _) = result
            self.result_resolution.set(f"resolution = {resolution}")
        else:
            self.result_resolution.set("Error!")
        super().on_update(result, exception)
    
    def on_update_draw(self, figure, result, exception):
        if result is not None:
            _, ((xd, xm), y, _), (peak_id, peak_im) = self.spectrum_process.peak_process.value
            smy = gaussian_filter(np.log(y + 1), 3.0)
            
            conf = self.process.conf
            band_range_xm = neighborhood(xm[peak_im], conf.res_band_radius)
            band_range_xd = neighborhood(xd[peak_id], conf.sp_band_radius)
            
            axe_peak = figure.add_subplot(1, 3, 1)
            axe_peak.imshow(smy, extent=[xm[0], xm[-1], xd[-1], xd[0]], cmap='Greys')
            axe_peak.contour(xm, xd, smy, colors='k')
            axe_peak.plot([xd[-1], xd[0]], [band_range_xm[0], band_range_xm[0]], '--', color='black')
            axe_peak.plot([xd[-1], xd[0]], [band_range_xm[1], band_range_xm[1]], '--', color='black')
            axe_peak.plot([band_range_xd[0], band_range_xd[0]], [xm[0], xm[-1]], '--', color='black')
            axe_peak.plot([band_range_xd[1], band_range_xd[1]], [xm[0], xm[-1]], '--', color='black')
            
            (sp_x, sp_y, _), (resolution, (res_x, res_y)) = result
            
            axe_sp = figure.add_subplot(1, 3, 2)
            axe_sp.set_title("spectrum")
            axe_sp.semilogy(sp_x, sp_y)
            
            axe_res = figure.add_subplot(1, 3, 3)
            axe_res.set_title("resolution")
            axe_res.semilogy(res_x, res_y)
        else:
            figure.gca().set_title("Error!")
            # todo show info
