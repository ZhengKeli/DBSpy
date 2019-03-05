import tkinter as tk

from spector.app.FrameController import FrameController


class SpectrumController(FrameController):
    def __init__(self, app, index):
        super().__init__(app)
        self.index = index
        self.process = app.process.spectrum_process_list[index]
        
        tk.Label(self.frame, text='This is a DBS Spectrum').pack()
        tk.Button(self.frame, text='Remove', foreground='red', command=self.on_remove).pack()
    
    def on_remove(self):
        del self.app.process.spectrum_process_list[self.index]
        self.app.update_frame(['main'])
        self.app.update_tree()
