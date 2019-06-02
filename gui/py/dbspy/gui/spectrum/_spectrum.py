import tkinter as tk

import matplotlib.pyplot as plt

from dbspy.gui import base


class Controller(base.ProcessController):
    def __init__(self, app, index):
        self.app = app
        self.index = index
        self.result_controller = None
        super().__init__(app.container, app.process.spectrum_processes[index])
    
    def on_create_info_frame(self, info_frame):
        tk.Label(info_frame, text='DBS Spectrum (tag=' + str(self.process.tag) + ')').pack()
        tk.Button(info_frame, text='Remove', foreground='red', command=self.remove).pack()
    
    def on_create_result_frame(self, result_frame):
        self.result_controller = base.FigureController(result_frame, plt.figure(), self.on_draw_result)
        self.result_controller.widget.pack(anchor='w', fill='both')
    
    def on_update(self, result, exception):
        self.result_controller.draw(result, exception)
    
    @staticmethod
    def on_draw_result(figure, result, exception):
        axe = figure.gca()
        if result is not None:
            (x, y, _), _ = result
            axe.semilogy(x, y)
        else:
            axe.set_title("Error!")
            # todo show info
    
    def remove(self):
        self.app.process.remove_spectrum_process(self.process)
        self.app.update_frame(['main'])
        self.app.update_tree()
