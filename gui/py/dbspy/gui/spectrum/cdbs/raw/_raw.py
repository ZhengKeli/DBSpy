import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndi

from dbspy.gui import base
from dbspy.gui.spectrum.dbs.raw._raw import Controller as DBSController


class Controller(DBSController):
    def on_create_result_frame(self, result_frame):
        self.result_controller = base.FigureController(result_frame, plt.figure(figsize=(5, 5)), self.on_update_draw)
        self.result_controller.widget.pack(fill='both')
    
    def on_update_draw(self, figure, result, exception):
        axe = figure.gca()
        if result is not None:
            (xi, xj), y = result
            smy = ndi.gaussian_filter(np.log(y + 1), 3.0)
            axe.imshow(smy, extent=[xj[0], xj[-1], xi[-1], xi[0]], cmap='Greys')
            axe.contour(xj, xi, smy, colors='k')
        else:
            axe.set_title("Error!")
            # todo show info
