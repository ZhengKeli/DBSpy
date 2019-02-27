import tkinter as tk


class SpectorFrameController:
    def __init__(self, app):
        self.spector_process = app.spector_process
        self.frame = tk.Frame(app.window)
        tk.Label(self.frame, text=f'You have {len(self.spector_process.spectrum_process_list)} spectrums.').pack()
        tk.Button(self.frame, text='New').pack()
