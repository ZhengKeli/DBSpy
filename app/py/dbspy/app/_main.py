import tkinter as tk

import dbspy.core as core
from dbspy.app import base


class Controller(base.ProcessController):
    def __init__(self, app):
        self.app = app
        self.spectrum_text = tk.StringVar()
        self.analyze_text = tk.StringVar()
        super().__init__(app.container, app.process)
    
    def on_create_info_frame(self, info_frame):
        pass
    
    def on_create_result_frame(self, result_frame):
        tk.Label(result_frame, textvariable=self.spectrum_text).pack(anchor='w')
        tk.Button(result_frame, text='New spectrum DBS', command=self.on_new_spectrum_dbs).pack(anchor='w')
        tk.Button(result_frame, text='New spectrum CDBS', command=self.on_new_spectrum_cdbs).pack(anchor='w')
        
        tk.Label(result_frame, textvariable=self.analyze_text).pack(anchor='w', pady='10p 0')
        tk.Button(result_frame, text='New analyze SW', command=self.on_new_analyze_sw).pack(anchor='w')
        tk.Button(result_frame, text='New analyze Ratio', command=self.on_new_analyze_ratio).pack(anchor='w')
    
    def on_update(self, result, exception):
        spectrum_len = len(self.process.spectrum_processes)
        self.spectrum_text.set(f'You have {spectrum_len} spectrum.')
        analyze_len = len(self.process.analyze_processes)
        self.analyze_text.set(f'You have {analyze_len} analyzes.')
    
    def on_new_spectrum_dbs(self):
        tag = '#' + str(len(self.process.spectrum_processes))
        new_spectrum_process = core.spectrum.dbs.Process(tag)
        self.process.append_spectrum_process(new_spectrum_process)
        self.app.update_tree()
    
    def on_new_spectrum_cdbs(self):
        tag = '#' + str(len(self.process.spectrum_processes))
        new_spectrum_process = core.spectrum.cdbs.Process(tag)
        self.process.append_spectrum_process(new_spectrum_process)
        self.app.update_tree()
    
    def on_new_analyze_sw(self):
        new_analyze_process = core.analyze.sw.Process(self.process.spectrum_cluster_block)
        self.process.append_analyze_process(new_analyze_process)
        self.app.update_tree()
    
    def on_new_analyze_ratio(self):
        new_analyze_process = core.analyze.ratio.Process(self.process.spectrum_cluster_block)
        self.process.append_analyze_process(new_analyze_process)
        self.app.update_tree()
