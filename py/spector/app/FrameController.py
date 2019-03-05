import abc
import tkinter as tk

from spector.app import Application


class FrameController:
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, app: Application):
        self.app = app
        self.frame = tk.Frame(app.container)
