import numpy as np

from spector.utils.Spectrum import Spectrum
from . import bg, peak, source, res


# define

class Conf:
    def __init__(self, source_conf: source.Conf, peak_conf: peak.Conf, bg_conf: bg.Conf, res_conf: res.Conf = None):
        self.source_conf = source_conf
        self.res_conf = res_conf
        self.peak_conf = peak_conf
        self.bg_conf = bg_conf


class Result:
    def __init__(self, sp_range_i, sp_spectrum, sp_resolution):
        self.sp_range_i = sp_range_i
        self.sp_spectrum = sp_spectrum
        self.sp_resolution = sp_resolution


class Context:
    def __init__(self):
        self.source_result: source.Result = None
        self.res_result: res.Result = None
        self.peak_result: peak.Result = None
        self.bg_result: bg.Result = None
        self.sp_result: Result = None


# process

def process(conf: Conf, context: Context = None) -> Result:
    source_result = source.process(conf.source_conf)
    raw_spectrum = source_result.raw_spectrum
    if context is not None:
        context.source_result = source_result
    
    if conf.res_conf is not None:
        res_result = res.process(raw_spectrum, conf.res_conf)
        resolution = res_result.resolution
        if context is not None:
            context.res_result = res_result
    else:
        resolution = None
    
    peak_result = peak.process(raw_spectrum, conf.peak_conf)
    peak_center_i = peak_result.peak_center_i
    peak_range_i = peak_result.peak_range_i
    peak_spectrum = peak_result.peak_spectrum
    if context is not None:
        context.peak_result = peak_result
    
    bg_result = bg.process(raw_spectrum, peak_center_i, peak_range_i, conf.bg_conf)
    bg_range_i = bg_result.bg_range_i
    bg_spectrum = bg_result.bg_spectrum
    if context is not None:
        context.bg_result = bg_result
    
    sp_range_i = peak_range_i
    sp_spectrum = subtract_bg(peak_range_i, peak_spectrum, bg_range_i, bg_spectrum)
    sp_result = Result(sp_range_i, sp_spectrum, resolution)
    if context is not None:
        context.sp_result = sp_result
    
    return sp_result


# utils

def subtract_bg(peak_range_i, peak_spectrum: Spectrum, bg_range_i, bg_spectrum: Spectrum):
    padding = max(bg_range_i[0] - peak_range_i[0], 0), max(peak_range_i[1] - bg_range_i[1], 0)
    cropping = max(peak_range_i[0] - bg_range_i[0], 0), max(bg_range_i[1] - peak_range_i[1], 0)
    
    bg_y = bg_spectrum.y
    bg_y = np.pad(bg_y, padding, 'edge')
    bg_y = bg_y[cropping[0]:len(bg_y) - cropping[1]]
    
    return Spectrum(peak_spectrum.x, peak_spectrum.y - bg_y, peak_spectrum.var)
