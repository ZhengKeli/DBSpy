import tkinter as tk
from tkinter import filedialog

from dbspy import base


class Controller(base.ProcessController):
    def __init__(self, app):
        self.app = app
        self.spectrum_text = tk.StringVar()
        self.analyze_text = tk.StringVar()
        super().__init__(app.container, app.process)
    
    def on_create_info_frame(self, info_frame):
        tk.Label(info_frame, textvariable=self.spectrum_text).pack(anchor='w')
        tk.Button(info_frame, text='New DBS spectrum', command=self.new_spectrum_dbs).pack(anchor='w')
        tk.Button(info_frame, text='New CDBS spectrum', command=self.new_spectrum_cdbs).pack(anchor='w')
        tk.Label(info_frame, textvariable=self.analyze_text).pack(anchor='w', pady=(10, 0))
        tk.Button(info_frame, text='New SW analyze', command=self.new_analyze_sw).pack(anchor='w')
        tk.Button(info_frame, text='New Curve analyze', command=self.new_analyze_curve).pack(anchor='w')
    
    def on_create_result_frame(self, result_frame):
        pass
    
    def on_update(self, result, exception):
        spectrum_len = len(self.process.spectrum_processes)
        self.spectrum_text.set(f'You have {spectrum_len} spectrum.')
        analyze_len = len(self.process.analyze_processes)
        self.analyze_text.set(f'You have {analyze_len} analyzes.')
    
    PENDING_TAGS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    PENDING_INDEX = -1
    
    @staticmethod
    def get_pending_tag():
        Controller.PENDING_INDEX += 1
        return Controller.PENDING_TAGS[Controller.PENDING_INDEX % len(Controller.PENDING_TAGS)]
    
    def new_spectrum_dbs(self):
        file_types = [('text file', '.txt'), ('all', '.*')]
        file_path = filedialog.askopenfilename(filetypes=file_types, defaultextension=file_types)
        
        tag = self.get_pending_tag()
        new_spectrum_process = dbspy.core.spectrum.dbs.Process(tag)
        new_spectrum_process.raw_process.conf = dbspy.core.spectrum.dbs.raw.Conf(file_path)
        
        self.process.append_spectrum_process(new_spectrum_process)
        self.update()
        self.app.update_tree()
    
    def new_spectrum_cdbs(self):
        file_types = [('text file', '.txt'), ('all', '.*')]
        file_path = filedialog.askopenfilename(filetypes=file_types, defaultextension=file_types)
        
        tag = self.get_pending_tag()
        new_spectrum_process = dbspy.core.spectrum.cdbs.Process(tag)
        new_spectrum_process.raw_process.conf = dbspy.core.spectrum.cdbs.raw.Conf(file_path)
        
        self.process.append_spectrum_process(new_spectrum_process)
        self.update()
        self.app.update_tree()
    
    def new_analyze_sw(self):
        new_analyze_process = dbspy.core.analyze.sw.Process(self.process.spectrum_cluster_block)
        self.process.append_analyze_process(new_analyze_process)
        self.update()
        self.app.update_tree()
    
    def new_analyze_curve(self):
        new_analyze_process = dbspy.core.analyze.curve.Process(self.process.spectrum_cluster_block)
        self.process.append_analyze_process(new_analyze_process)
        self.update()
        self.app.update_tree()
