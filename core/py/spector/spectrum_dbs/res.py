import numpy as np

from spector.utils.gaussian import gaussian_fwhm, gaussian_fit
from spector.utils.spectrum import Spectrum
from .peak import Conf
from .peak import process as peak_process


# define

class Result:
    def __init__(self, resolution):
        self.resolution = resolution


# process

def process(sp: Spectrum, conf: Conf) -> Result:
    peak_result = peak_process(sp, conf)
    resolution = compute_resolution(peak_result.peak_range_i, peak_result.peak_center_i, peak_result.peak_spectrum)
    return Result(resolution)


# utils

def compute_resolution(peak_range_i, peak_center_i, peak_spectrum):
    xs = peak_spectrum.x
    xs = xs - xs[peak_center_i - peak_range_i[0]]
    ys = peak_spectrum.y
    points = np.stack((xs, ys), 1)
    resolution = gaussian_fwhm(gaussian_fit(points))
    return resolution
