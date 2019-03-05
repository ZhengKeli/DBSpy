import numpy as np

from spector.core.base import BaseProcess
from spector.utils.spectrum import Spectrum
from . import bg, peak, raw, res


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
    
    def __init__(self, raw_process=None, res_process=None, peak_process=None, bg_process=None):
        super().__init__()
        self.raw_process = raw.Process() if raw_process is None else raw_process
        self.res_process = None if res_process is None else res_process
        self.peak_process = peak.Process() if peak_process is None else peak_process
        self.bg_process = bg.Process() if bg_process is None else bg_process
    
    @staticmethod
    def from_conf(conf: Conf):
        raw_process = raw.Process(conf.raw_conf)
        peak_process = peak.Process(conf.peak_conf)
        bg_process = bg.Process(conf.bg_conf)
        res_process = None if conf.res_conf is None else res.Process(conf.res_conf)
        return Process(raw_process, res_process, peak_process, bg_process)
    
    def on_process(self):
        raw_spectrum = self.raw_process.process()
        
        if self.res_process is not None:
            resolution = self.res_process.process(raw_spectrum)
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
