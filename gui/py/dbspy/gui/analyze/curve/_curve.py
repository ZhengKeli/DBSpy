import tkinter as tk
import tkinter.ttk as ttk

import matplotlib.pyplot as plt
import numpy as np

from dbspy.core.analyze.curve import Conf
from dbspy.gui import base
from dbspy.gui._app import Application
from dbspy.gui.utils.figure import FigureResultController


class Controller(FigureResultController, base.ElementProcessController):
    def __init__(self, app, index):
        self.app: Application = app
        self.index = index
        self.conf_fold_mode = tk.StringVar()
        self.conf_compare_mode = tk.StringVar()
        super().__init__(
            app.container,
            app.process.analyze_processes[index],
            plt.figure(figsize=(7, 5)))
    
    def on_create_info_frame(self, info_frame):
        tk.Label(info_frame, text='Curve Analyze').pack()
        tk.Button(info_frame, text='Remove', foreground='red', command=self.remove).pack()
    
    def on_create_conf_frame(self, conf_frame):
        tk.Label(conf_frame, text="fold_mode=").pack(side='left')
        ttk.OptionMenu(conf_frame, self.conf_fold_mode, 'fold', *Conf.fold_modes).pack(side='left')
        tk.Label(conf_frame, text="compare_mode=").pack(side='left', padx=(10, 0))
        ttk.OptionMenu(conf_frame, self.conf_compare_mode, 'ratio', *Conf.compare_modes).pack(side='left')
    
    def on_reset(self, conf: Conf):
        self.conf_fold_mode.set(conf.fold_mode)
        self.conf_compare_mode.set(conf.compare_mode)
    
    def on_apply(self) -> Conf:
        return Conf(
            fold_mode=self.conf_fold_mode.get(),
            compare_mode=self.conf_compare_mode.get())
    
    def on_update_draw(self, figure, result, exception):
        axe = figure.gca()
        if result is not None:
            tag_list = tuple(process.tag for process in self.app.process.spectrum_processes)
            curve_list, _ = result
            conf = self.process.conf
            
            axe.set_title("Curves")
            for i, (x, curve, curve_var) in enumerate(curve_list):
                if i == conf.control_index:
                    axe.plot(x, curve, '--', color='gray')
                else:
                    axe.errorbar(x, curve, np.sqrt(curve_var), fmt='.', capsize=3)
            axe.legend(tag_list)
            
            if conf.compare_mode == 'ratio':
                axe.set_ylim(0.7, 2.0)
        else:
            figure.gca().set_title("Error!")
            # todo show info
    
    def remove(self):
        self.app.process.remove_analyze_process(self.process)
        self.app.update_frame(['main'])
        self.app.update_tree()
