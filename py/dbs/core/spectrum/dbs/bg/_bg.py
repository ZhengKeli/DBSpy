import numpy as np

from dbs.core import base
from dbs.utils.spectrum import Spectrum


# define

class Conf(base.ElementConf):
    def __init__(self, bg_radius=None, bg_range=None, bg_expand=None, bg_algorithm=None):
        self.radius = bg_radius
        self.range = bg_range
        self.bg_expand = bg_expand
        self.bg_algorithm = bg_algorithm


class Process(base.ElementProcess):
    def __init__(self, raw_process, peak_process):
        super().__init__(process_func, Conf(), raw_process.block, peak_process.block)


def process_func(raw_result, peak_res, conf: Conf):
    raw_sp = Spectrum(*raw_result)
    peak_range_i, _, peak_center_i = peak_res
    
    if conf.range is not None:
        bg_range = conf.range
        bg_range_i = raw_sp.index(bg_range[0]), raw_sp.index(bg_range[1])
    elif conf.radius is not None:
        peak_center = raw_sp.x[peak_center_i + peak_range_i[0]]
        bg_range = (peak_center - conf.radius, peak_center + conf.radius)
        bg_range_i = raw_sp.index(bg_range[0]), raw_sp.index(bg_range[1])
    else:
        bg_range_i = peak_range_i
        bg_range = raw_sp.x[peak_range_i[0]], raw_sp.x[peak_range_i[1]]
    
    bg_expand = 0.0 if conf.bg_expand is None else conf.bg_expand
    if isinstance(bg_expand, float) or isinstance(bg_expand, int):
        bg_expand = [bg_expand, bg_expand]
    
    expanded_range = bg_range[0] - bg_expand[0], bg_range[1] + bg_expand[1]
    ex_range_i = raw_sp.index(expanded_range[0]), raw_sp.index(expanded_range[1])
    
    bg_algorithm = conf.bg_algorithm
    if bg_algorithm == 'volumeLinear' or bg_algorithm is None:
        bg_y = volume_linear_bg(raw_sp.y, *bg_range_i, *ex_range_i)
        bg_spectrum = Spectrum(raw_sp.x[slice(*bg_range_i)], bg_y)
    else:
        raise TypeError(f"not supported bg_type:{type(conf)}")
    
    return bg_range_i, bg_spectrum


# utils

def volume_linear_bg(ys, bg_head_i, bg_tail_i, expanded_head_i, expanded_tail_i):
    # head & tail
    head_bg = np.mean(ys[expanded_head_i: bg_head_i + 1])
    tail_bg = np.mean(ys[bg_tail_i - 1:expanded_tail_i])
    
    # center
    bg_y = np.repeat(np.expand_dims(head_bg, 0), bg_tail_i - bg_head_i, axis=0)
    sum_area = np.sum(ys[bg_head_i:bg_tail_i])
    scan_area = 0
    for i in range(len(bg_y)):
        scan_area += ys[bg_head_i + i]
        bg_y[i] += (tail_bg - head_bg) * scan_area / sum_area
    
    return bg_y
