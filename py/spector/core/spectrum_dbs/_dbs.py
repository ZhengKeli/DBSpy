import numpy as np

from . import bg, peak, raw, res
from ..utils import BaseProcess
from ..utils import Spectrum


# define

class Conf:
    def __init__(self, raw_conf: raw.Conf, peak_conf: peak.Conf, bg_conf: bg.Conf, res_conf: res.Conf = None):
        self.raw_conf = raw_conf
        self.peak_conf = peak_conf
        self.bg_conf = bg_conf
        self.res_conf = res_conf


class Result:
    def __init__(self, sp_range_i, sp_spectrum, sp_resolution):
        self.sp_range_i = sp_range_i
        self.sp_spectrum = sp_spectrum
        self.sp_resolution = sp_resolution


class Process(BaseProcess):
    
    def __init__(self, conf: Conf):
        super().__init__()
        self.conf = conf
        self.raw_process = raw.Process(conf.raw_conf)
        self.peak_process = peak.Process(conf.peak_conf)
        self.bg_process = bg.Process(conf.bg_conf)
        self.res_process = None if conf.res_conf is None else res.Process(conf.res_conf)
    
    def on_process(self):
        source_result = self.raw_process.process()
        raw_spectrum = source_result.raw_spectrum
    
        if self.res_process is not None:
            res_result = self.res_process.process(raw_spectrum)
            resolution = res_result.resolution
        else:
            resolution = None
    
        peak_result = self.peak_process.process(raw_spectrum)
        peak_center_i = peak_result.peak_center_i
        peak_range_i = peak_result.peak_range_i
        peak_spectrum = peak_result.peak_spectrum
    
        bg_result = self.bg_process.process(raw_spectrum, peak_center_i, peak_range_i)
        bg_range_i = bg_result.bg_range_i
        bg_spectrum = bg_result.bg_spectrum
        
        sp_range_i = peak_range_i
        sp_spectrum = subtract_bg(peak_range_i, peak_spectrum, bg_range_i, bg_spectrum)
        sp_result = Result(sp_range_i, sp_spectrum, resolution)
        return sp_result


# utils

def subtract_bg(peak_range_i, peak_spectrum: Spectrum, bg_range_i, bg_spectrum: Spectrum):
    padding = max(bg_range_i[0] - peak_range_i[0], 0), max(peak_range_i[1] - bg_range_i[1], 0)
    cropping = max(peak_range_i[0] - bg_range_i[0], 0), max(bg_range_i[1] - peak_range_i[1], 0)
    
    bg_y = bg_spectrum.y
    bg_y = np.pad(bg_y, padding, 'edge')
    bg_y = bg_y[cropping[0]:len(bg_y) - cropping[1]]
    
    return Spectrum(peak_spectrum.x, peak_spectrum.y - bg_y, peak_spectrum.var)