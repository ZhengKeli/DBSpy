import numpy as np

from dbs.core import base
from dbs.core.spectrum.dbs.peak import _peak as peak
from dbs.utils.gaussian import gaussian_fwhm, gaussian_fit
from dbs.utils.spectrum import Spectrum


# define

class Conf(peak.Conf):
    pass


class Process(base.ElementProcess):
    def __init__(self, raw_process):
        super().__init__(process_func, Conf(), raw_process.block)


def process_func(raw_sp: Spectrum, conf: Conf) -> float:
    peak_range_i, peak_spectrum, peak_center_i = peak.process_func(raw_sp, conf)
    resolution = compute_resolution(peak_range_i, peak_center_i + peak_range_i[0], peak_spectrum)
    return resolution


# utils

def compute_resolution(peak_range_i, peak_center_i, peak_spectrum):
    xs = peak_spectrum.x
    xs = xs - xs[peak_center_i - peak_range_i[0]]
    ys = peak_spectrum.y
    points = np.stack((xs, ys), 1)
    resolution = gaussian_fwhm(gaussian_fit(points))
    return resolution
