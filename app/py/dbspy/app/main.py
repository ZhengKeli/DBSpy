import tkinter as tk

import dbspy.core as core
from dbspy.app.base import BaseController
from dbspy.core import Process


class MainController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.process: Process = app.process
        
        self.spectrum_text = tk.StringVar()
        self.analyze_text = tk.StringVar()

        tk.Label(self.frame, textvariable=self.spectrum_text).pack(anchor='w')
        tk.Button(self.frame, text='New spectrum DBS', command=self.on_new_spectrum_dbs).pack(anchor='w')
        tk.Button(self.frame, text='New spectrum CDBS', state='disabled', command=self.on_new_spectrum_cdbs).pack(
            anchor='w')
        
        tk.Label(self.frame, textvariable=self.analyze_text).pack(anchor='w', pady='10p 0')
        tk.Button(self.frame, text='New analyze SW', command=self.on_new_analyze_sw).pack(anchor='w')
        tk.Button(self.frame, text='New analyze Ratio', command=self.on_new_analyze_ratio).pack(anchor='w')

        self.reset()

    def reset(self):
        spectrum_len = len(self.process.spectrum_processes)
        self.spectrum_text.set(f'You have {spectrum_len} spectrums.')
        analyze_len = len(self.process.analyze_processes)
        self.analyze_text.set(f'You have {analyze_len} analyzes.')
    
    def on_new_spectrum_dbs(self):
        new_spectrum_process = core.spectrum.dbs.Process()
        self.process.spectrum_processes += [new_spectrum_process]
        self.app.update_tree()

    def on_new_spectrum_cdbs(self):
        raise RuntimeError("CDBS spectrums currently not supported")

    def on_new_analyze_sw(self):
        new_analyze_process = core.analyze.sw.Process(self.process.spectrum_cluster_block)
        self.process.analyze_processes += [new_analyze_process]
        self.app.update_tree()

    def on_new_analyze_ratio(self):
        new_analyze_process = core.analyze.ratio.Process(self.process.spectrum_cluster_block)
        self.process.analyze_processes += [new_analyze_process]
        self.app.update_tree()
