import abc
import tkinter as tk
from typing import Optional

from matplotlib import pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from dbspy.core.base import Process
from dbspy.gui.base import WidgetController, ProcessController


class FigureController(WidgetController):
    def __init__(self, master: tk.Frame, figure: plt.Figure, on_draw: callable):
        self.figure = figure
        self.on_draw = on_draw
        canvas = FigureCanvasTkAgg(figure, master)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, master)
        toolbar.update()
        super().__init__(canvas.get_tk_widget())
    
    def draw(self, *content):
        self.figure.clear()
        self.on_draw(self.figure, *content)
        self.figure.tight_layout()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()


class FigureResultController(ProcessController, abc.ABC):
    def __init__(self, master: tk.Frame, process: Process, result_figure: Optional[plt.Figure]):
        self.result_figure = plt.Figure() if result_figure is None else result_figure
        self.result_controller = None
        super().__init__(master, process)
    
    def on_create_result_frame(self, result_frame):
        self.result_controller = FigureController(result_frame, self.result_figure, self.on_update_draw)
        self.result_controller.widget.pack(fill='both')
    
    def on_update(self, result, exception):
        self.update_draw(result, exception)
    
    def update_draw(self, result, exception):
        self.result_controller.draw(result, exception)
    
    @abc.abstractmethod
    def on_update_draw(self, figure, result, exception):
        pass
