import tkinter as tk

import spector.core as core
from spector.app.base import BaseController


class MainController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.process: core.MainProcess = app.process

        self.spectrum_text = tk.StringVar()
        self.artifact_text = tk.StringVar()

        tk.Label(self.frame, textvariable=self.spectrum_text).pack(anchor='w')
        tk.Button(self.frame, text='New spectrum DBS', command=self.on_new_spectrum_dbs).pack(anchor='w')
        tk.Button(self.frame, text='New spectrum CDBS', state='disabled', command=self.on_new_spectrum_cdbs).pack(anchor='w')

        tk.Label(self.frame, textvariable=self.artifact_text).pack(anchor='w', pady='10p 0')
        tk.Button(self.frame, text='New artifact SW', command=self.on_new_artifact_sw).pack(anchor='w')
        tk.Button(self.frame, text='New artifact Ratio', command=self.on_new_artifact_ratio).pack(anchor='w')

        self.reset()

    def reset(self):
        spectrum_len = len(self.process.spectrum_process_list)
        self.spectrum_text.set(f'You have {spectrum_len} spectrums.')
        artifact_len = len(self.process.artifact_process_list)
        self.artifact_text.set(f'You have {artifact_len} artifacts.')
    
    def on_new_spectrum_dbs(self):
        new_spectrum_process = core.spectrum.dbs.Process()
        self.process.spectrum_process_list.append(new_spectrum_process)
        self.app.update_tree()

    def on_new_spectrum_cdbs(self):
        raise RuntimeError("CDBS spectrums currently not supported")

    def on_new_artifact_sw(self):
        new_artifact_process = core.artifact.sw.Process()
        self.process.artifact_process_list.append(new_artifact_process)
        self.app.update_tree()

    def on_new_artifact_ratio(self):
        new_artifact_process = core.artifact.ratio.Process()
        self.process.artifact_process_list.append(new_artifact_process)
        self.app.update_tree()
