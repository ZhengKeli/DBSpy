import tkinter as tk

import spector.core as core


class MainFrameController:
    def __init__(self, app):
        self.app = app
        self.process: core.main.Process = app.process
        self.frame = tk.Frame(app.window)
        
        spectrum_len = len(self.app.process.spectrum_process_list)
        tk.Label(self.frame, text=f'You have {spectrum_len} spectrums.').pack()
        tk.Button(self.frame, text='New', command=self.on_new_spectrum).pack()
    
    def on_new_spectrum(self):
        # todo create a spectrum
        # process = core.spectrum_dbs.Process()
        # self.app.process.spectrum_process_list.append(process)
        pass
