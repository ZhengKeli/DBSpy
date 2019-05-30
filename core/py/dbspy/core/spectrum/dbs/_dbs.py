import numpy as np

from dbspy.core.spectrum import _spectrum as spectrum
from dbspy.utils.block import FunctionBlock
from . import bg, peak, raw, res


# define
class Conf(spectrum.Conf):
    def __init__(self, tag=None, raw_conf=None, res_conf=None, peak_conf=None, bg_conf=None):
        super().__init__(tag)
        self.raw = raw_conf
        self.res = res_conf
        self.peak = peak_conf
        self.bg = bg_conf
    
    def create_process(self):
        return Process(self.tag)
    
    def encode_content(self):
        return {
            'raw': self.raw.encode(),
            'res': self.res.encode(),
            'peak': self.peak.encode(),
            'bg': self.bg.encode()}
    
    @classmethod
    def decode_content(cls, code):
        return cls(
            raw.Conf.decode(code['raw']),
            res.Conf.decode(code['res']),
            peak.Conf.decode(code['peak']),
            bg.Conf.decode(code['bg']))


class Process(spectrum.Process):
    def __init__(self, tag):
        self.raw_process = raw.Process()
        self.res_process = res.Process(self.raw_process)
        self.peak_process = peak.Process(self.raw_process)
        self.bg_process = bg.Process(self.raw_process, self.peak_process)
        integrate_block = FunctionBlock(
            integrate_func,
            self.res_process.block,
            self.peak_process.block,
            self.bg_process.block)
        super().__init__(integrate_block, tag)
    
    @property
    def conf(self) -> Conf:
        return Conf(
            self.tag,
            self.raw_process.conf,
            self.res_process.conf,
            self.peak_process.conf,
            self.bg_process.conf)
    
    @conf.setter
    def conf(self, conf: Conf):
        self.tag = conf.tag
        self.raw_process.conf = conf.raw
        self.res_process.conf = conf.res
        self.peak_process.conf = conf.peak
        self.bg_process.conf = conf.bg


def integrate_func(res_result, peak_result, bg_result):
    resolution = res_result
    peak_range_i, peak_spectrum, _ = peak_result
    bg_range_i, bg_spectrum = bg_result
    sp_spectrum = subtract_bg(peak_range_i, peak_spectrum, bg_range_i, bg_spectrum)
    return sp_spectrum, resolution


# utils

def subtract_bg(peak_range_i, peak_spectrum, bg_range_i, bg_spectrum):
    peak_x, peak_y, peak_var = peak_spectrum
    _, bg_y = bg_spectrum
    
    padding = max(bg_range_i[0] - peak_range_i[0], 0), max(peak_range_i[1] - bg_range_i[1], 0)
    cropping = max(peak_range_i[0] - bg_range_i[0], 0), max(bg_range_i[1] - peak_range_i[1], 0)
    
    bg_y = np.pad(bg_y, padding, 'edge')
    bg_y = bg_y[cropping[0]:len(bg_y) - cropping[1]]
    
    return peak_x, peak_y - bg_y, peak_var
