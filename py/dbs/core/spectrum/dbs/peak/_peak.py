import numpy as np

from dbs.core.base import BaseProcess
from dbs.utils.spectrum import Spectrum


# define

class Conf:
    def __init__(self, search_center=None, search_radius=None, search_range=None, peak_center=None, peak_radius=None):
        self.search_center = search_center
        self.search_radius = search_radius
        self.search_range = search_range
        self.peak_center = peak_center
        self.peak_radius = peak_radius


class Result:
    def __init__(self, peak_center_i, peak_range_i, peak_spectrum: Spectrum):
        self.peak_center_i = peak_center_i
        self.peak_range_i = peak_range_i
        self.peak_spectrum = peak_spectrum


class Process(BaseProcess):
    
    def __init__(self, conf: Conf = None):
        super().__init__()
        self.conf = Conf() if conf is None else conf
    
    def on_process(self, sp: Spectrum):
        return process(sp, self.conf)


# process

def process(sp: Spectrum, conf: Conf):
    if conf.search_range is not None:
        search_range = conf.search_range
    elif conf.search_center is not None and conf.search_radius is not None:
        search_range = (conf.search_center - conf.search_radius, conf.search_center + conf.search_radius)
    else:
        search_range = None
    
    if conf.peak_radius is not None:
        peak_radius = conf.peak_radius
    elif conf.search_radius is not None:
        peak_radius = conf.search_radius
    else:
        raise RuntimeError("Cannot define the radius of peak.")
    
    if conf.peak_center is not None:
        peak_center = conf.peak_center
        peak_center_i = sp.index(peak_center)
    elif search_range is not None:
        peak_center_i = search_peak_center_i(sp.y, sp.index(search_range[0]), sp.index(search_range[1]))
        peak_center = sp.x[peak_center_i]
    else:
        raise RuntimeError("Cannot define the index of peak center.")
    
    peak_range = (peak_center - peak_radius, peak_center + peak_radius)
    peak_range_i = sp.index(peak_range[0]), sp.index(peak_range[1])
    peak_spectrum = sp[slice(*peak_range_i)]
    return Result(peak_center_i, peak_range_i, peak_spectrum)


# utils

def search_peak_center_i(ys, search_head_i, search_tail_i):
    search_ys = ys[search_head_i:search_tail_i]
    peak_center_i = np.argmax(search_ys) + search_head_i
    return peak_center_i
