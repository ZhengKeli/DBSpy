import numpy as np

from dbspy.core import base
from dbspy.core.spectrum.dbs.peak import _peak as peak
from dbspy.core.utils.gaussian import gaussian_fwhm, gaussian_fit
from dbspy.core.utils.neighborhood import neighborhood


# define

class Conf(peak.Conf):
    def __init__(self, search_range=neighborhood(1157, 5), peak_radius=7):
        super().__init__(search_range, peak_radius)


class Process(base.ElementProcess):
    def __init__(self, raw_process):
        super().__init__(process_func, Conf(), raw_process.block)


def process_func(raw_result, conf: Conf):
    peak_range_i, (peak_x, peak_y, _), peak_center_i = peak.process_func(raw_result, conf)
    resolution = compute_resolution(peak_x, peak_y, peak_center_i)
    return resolution, ((peak_x, peak_y), peak_center_i)


# utils

def compute_resolution(x, y, peak_i):
    points = np.stack((x - x[peak_i], y), 1)
    resolution = gaussian_fwhm(gaussian_fit(points))
    return resolution
