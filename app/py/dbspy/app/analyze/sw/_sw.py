import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from dbspy.app import base
from dbspy.core.analyze.sw import Conf


class Controller(base.ElementProcessController):
    def __init__(self, app, index):
        self.main_process = app.process
        self.index = index
        self.conf_rs = tk.StringVar()
        self.conf_rw = tk.StringVar()
        self.conf_ra = tk.StringVar()
        self.result_figure: plt.Figure = plt.figure(figsize=(7, 6))
        super().__init__(app.container, app.process.analyze_processes[index])
    
    def on_create_info_frame(self, info_frame):
        tk.Label(info_frame, text='SW Analyze').pack()
    
    def on_create_conf_frame(self, conf_frame):
        tk.Label(conf_frame, text='rs=').pack(side='left')
        tk.Entry(conf_frame, textvariable=self.conf_rs, width=4).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
        
        tk.Label(conf_frame, text='rw=').pack(side='left', padx=(10, 0))
        tk.Entry(conf_frame, textvariable=self.conf_rw, width=4).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
        
        tk.Label(conf_frame, text='ra=').pack(side='left', padx=(10, 0))
        tk.Entry(conf_frame, textvariable=self.conf_ra, width=4).pack(side='left')
        tk.Label(conf_frame, text='eV').pack(side='left')
    
    def on_create_result_frame(self, result_frame):
        canvas = FigureCanvasTkAgg(self.result_figure, result_frame)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, result_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(anchor='w', fill='both')
    
    def on_reset(self, conf: Conf):
        self.conf_rs.set('0.0' if conf.s_radius is None else str(conf.s_radius))
        self.conf_rw.set('0.0' if conf.w_radius is None else str(conf.w_radius))
        self.conf_ra.set('0.0' if conf.a_radius is None else str(conf.a_radius))
    
    def on_apply(self) -> Conf:
        return Conf(
            s_radius=float(self.conf_rw.get()),
            w_radius=float(self.conf_ra.get()),
            a_radius=float(self.conf_rs.get()))
    
    def on_update(self, result, exception):
        self.result_figure.clear()
        if result is not None:
            tag_list = tuple(process.tag for process in self.main_process.spectrum_processes)
            s_list, s_var_list, w_list, w_var_list = zip(*(
                (s, s_var, w, w_var) for (s, s_var, _), (w, w_var, _) in result))
            
            sp_index = 0
            (x, y, _), _ = self.main_process.spectrum_processes[sp_index].value
            (_, _, s_range_i), (_, _, w_range_i) = result[sp_index]
            peak_i = np.argmax(y)
            
            axe_sp = self.result_figure.add_subplot(2, 1, 1)
            axe_s = self.result_figure.add_subplot(2, 2, 3)
            axe_w = self.result_figure.add_subplot(2, 2, 4)
            
            axe_sp.fill_between(x[slice(*s_range_i)], y[slice(*s_range_i)], color='#0088ff')
            if isinstance(w_range_i[0], tuple):
                w1_range_i, w2_range_i = w_range_i
                axe_sp.fill_between(x[slice(*w1_range_i)], y[slice(*w1_range_i)], color='#ff8800')
                axe_sp.fill_between(x[slice(*w2_range_i)], y[slice(*w2_range_i)], color='#ff8800')
            else:
                axe_sp.fill_between(x[slice(*w_range_i)], y[slice(*w_range_i)], color='#ff8800')
            
            axe_sp.plot(x, y, color='black')
            axe_sp.plot([x[peak_i], x[peak_i]], [0, y[peak_i]], '--', color='black')
            
            axe_s.set_title("S")
            axe_s.errorbar(tag_list, s_list, np.sqrt(s_var_list), capsize=3, fmt='.-', color='#0088ff')
            axe_w.set_title("W")
            axe_w.errorbar(tag_list, w_list, np.sqrt(w_var_list), capsize=3, fmt='.-', color='#ff8800')
        else:
            self.result_figure.gca().set_title("Error!")
            # todo show info
        self.result_figure.tight_layout()
        self.result_figure.canvas.draw()
        self.result_figure.canvas.flush_events()
