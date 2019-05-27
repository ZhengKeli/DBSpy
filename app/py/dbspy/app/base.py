import abc
import tkinter as tk


class BaseController:
    __metaclass__ = abc.ABCMeta

    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.container)
