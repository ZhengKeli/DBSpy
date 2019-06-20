import tkinter as tk

import matplotlib.pyplot as plt

from dbspy.gui import base
from dbspy.gui.utils.figure import FigureController


class Controller(base.ProcessController):
    def __init__(self, app, index):
        self.app = app
        self.index = index
        self.result_controller = None
        self.conf_tag = tk.Variable()
        super().__init__(app.container, app.process.spectrum_processes[index])
    
    def on_create_info_frame(self, info_frame):
        tk.Label(info_frame, text='DBS Spectrum').pack()
        
        tag_frame = tk.Frame(info_frame)
        tk.Label(tag_frame, text='tag=').pack(side='left')
        tk.Entry(tag_frame, width=6, textvariable=self.conf_tag).pack(side='left')
        tk.Button(tag_frame, text='OK', command=self.apply_tag).pack(side='left')
        tag_frame.pack()
        
        tk.Button(info_frame, text='Remove', foreground='red', command=self.remove).pack()
    
    def on_create_result_frame(self, result_frame):
        self.result_controller = FigureController(result_frame, plt.figure(), self.on_draw_result)
        self.result_controller.widget.pack(anchor='w', fill='both')
    
    def on_update(self, result, exception):
        self.conf_tag.set(str(self.process.tag))
        self.result_controller.draw(result, exception)
    
    @staticmethod
    def on_draw_result(figure, result, _):
        axe = figure.gca()
        if result is not None:
            (x, y, _), _ = result
            axe.semilogy(x, y)
        else:
            axe.set_title("Error!")
            # todo show info
    
    def apply_tag(self):
        tag = self.conf_tag.get()
        try:
            tag = int(tag)
        except ValueError:
            try:
                tag = float(tag)
            except ValueError:
                pass
        self.process.tag = tag
        self.app.update_tree()
    
    def remove(self):
        self.app.process.remove_spectrum_process(self.process)
        self.app.update_frame(['main'])
        self.app.update_tree()
