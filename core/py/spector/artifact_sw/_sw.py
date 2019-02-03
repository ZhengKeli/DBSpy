from typing import Iterable

import numpy as np

from spector.utils.indexing import search_nearest
from spector.utils.spectrum import Spectrum
from spector.utils.variance import add_var, sum_var, divide_var


# define

class Conf:
    def __init__(self, s_radius=None, w_radius=None, control_s=None, control_w=None):
        self.s_radius = s_radius
        self.w_radius = w_radius
        self.control_s = control_s
        self.control_w = control_w


class ResultItem:
    def __init__(self, s, s_var, s_range_i, w, w_var, w_range_i, w1, w1_var, w1_range, w2, w2_var, w2_range):
        self.s = s
        self.s_var = s_var
        self.s_range_i = s_range_i
        
        self.w = w
        self.w_var = w_var
        self.w_range_i = w_range_i
        
        self.w2 = w2
        self.w2_var = w2_var
        self.w2_range = w2_range
        
        self.w1 = w1
        self.w1_var = w1_var
        self.w1_range = w1_range


class Result:
    def __init__(self, items: Iterable[ResultItem]):
        self.result_list = items


# process

def process(sp_list: Iterable[Spectrum], conf: Conf) -> Result:
    result_list = []
    control_s_radius = None
    control_w_radius = None
    for sp in sp_list:
        sum_ys = np.sum(sp.y)
        
        center_i = np.argmax(sp.y)
        center = sp.x[center_i]
        
        if conf.s_radius is not None:
            s_radius = conf.s_radius
        elif conf.control_s is not None:
            if control_s_radius is None:
                control_s_radius_i = surround_nearest(sp.y, center_i, conf.control_s * sum_ys)
                control_s_radius = (sp.x[center_i + control_s_radius_i] - sp.x[center_i - control_s_radius_i]) / 2.0
            s_radius = control_s_radius
        else:
            raise TypeError("Can not define s_radius by the conf.")
        s_range = center - s_radius, center + s_radius
        s_range_i = sp.index(s_range)
        
        if conf.w_radius is not None:
            w_radius = conf.w_radius
        elif conf.control_w is not None:
            if control_w_radius is None:
                control_w_radius_i = surround_nearest(sp.y, center_i, (1.0 - conf.control_w) * sum_ys)
                control_w_radius = (sp.x[center_i + control_w_radius_i] - sp.x[center_i - control_w_radius_i]) / 2.0
            w_radius = control_w_radius
        else:
            raise TypeError("Can not define w_radius by the conf.")
        w_range = center - w_radius, center + w_radius
        w_range_i = sp.index(w_range)
        
        s, s_var = rate_var(sp.y, sp.var, s_range_i[0], s_range_i[1])
        w1, w1_var = rate_var(sp.y, sp.var, None, w_range_i[0])
        w2, w2_var = rate_var(sp.y, sp.var, w_range_i[1], None)
        w, w_var = add_var(w1, w1_var, w2, w2_var)
        result = ResultItem(
            s, s_var, s_range_i,
            w, w_var, w_range_i,
            w1, w1_var, (0, w_range_i[0]),
            w2, w2_var, (w_range_i[0], len(sp)))
        result_list.append(result)
    return Result(result_list)


# utils

def surround_nearest(ys, center_i, s):
    nearest_radius_i, _ = search_nearest(
        0, min(center_i, len(ys) - center_i) + 1, 1, s,
        lambda radius_i: np.sum(ys[center_i - radius_i:center_i + radius_i]))
    return nearest_radius_i


def rate_var(ys, ys_var, head, tail):
    if head is None:
        head = 0
    
    if tail is None:
        tail = len(ys)
    
    if not (0 <= head <= tail <= len(ys)):
        raise RuntimeError("Index out of bounds.")
    
    a, a_var = sum_var(ys, ys_var)
    s, s_var = sum_var(ys[head:tail], ys_var[head:tail])
    return divide_var(s, s_var, a, a_var)
