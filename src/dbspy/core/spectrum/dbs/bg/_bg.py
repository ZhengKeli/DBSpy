from collections import Iterable

import numpy as np

from dbspy.core import base
from dbspy.core.utils.indexing import index_nearest


# define

class Conf(base.ElementConf):
    bg_algorithms = ('volumeLinear',)
    
    def __init__(self, bg_radius=15, bg_range=None, bg_expand=(1, 1), bg_algorithm='volumeLinear'):
        self.bg_radius = bg_radius
        self.bg_range = bg_range
        self.bg_expand = bg_expand
        self.bg_algorithm = bg_algorithm


class Process(base.ElementProcess):
    def __init__(self, raw_process, peak_process):
        super().__init__(process_func, Conf(), raw_process.block, peak_process.block)


def process_func(raw_result, peak_res, conf: Conf):
    raw_x, raw_y = raw_result
    peak_range_i, _, peak_center_i = peak_res
    
    if conf.bg_range is not None:
        bg_range = conf.bg_range
        bg_range_i = index_nearest(bg_range, raw_x)
    elif conf.bg_radius is not None:
        peak_center = raw_x[peak_center_i + peak_range_i[0]]
        bg_range = (peak_center - conf.bg_radius, peak_center + conf.bg_radius)
        bg_range_i = index_nearest(bg_range, raw_x)
    else:
        bg_range_i = peak_range_i
        bg_range = raw_x[bg_range_i[0]], raw_x[bg_range_i[1]]
    
    bg_expand = 0.0 if conf.bg_expand is None else conf.bg_expand
    if not isinstance(bg_expand, Iterable):
        bg_expand = (bg_expand, bg_expand)
    
    expanded_range = bg_range[0] - bg_expand[0], bg_range[1] + bg_expand[1]
    ex_range_i = index_nearest(expanded_range, raw_x)
    
    bg_algorithm = conf.bg_algorithm
    if bg_algorithm == 'volumeLinear':
        bg_y = volume_linear_bg(raw_y, *bg_range_i, *ex_range_i)
        bg_x = raw_x[slice(*bg_range_i)]
    else:
        raise TypeError(f"not supported bg_type:{type(conf)}")
    
    return bg_range_i, (bg_x, bg_y)


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
