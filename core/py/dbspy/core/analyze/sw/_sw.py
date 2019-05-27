from typing import Iterable

import numpy as np

from dbspy.core import base
from dbspy.core.analyze import _analyze as analyze
from dbspy.utils.indexing import search_nearest
from dbspy.utils.spectrum import Spectrum
from dbspy.utils.variance import add_var, sum_var, divide_var


# define

class Conf(analyze.Conf):
    def __init__(self, a_radius=None, s_radius=None, w_radius=None, control_id=None, control_s=None, control_w=None):
        self.a_radius = a_radius
        self.s_radius = s_radius
        self.w_radius = w_radius
        self.control_id = control_id
        self.control_s = control_s
        self.control_w = control_w

    @staticmethod
    def create_process(cluster_block):
        return Process(cluster_block)


class Process(base.ElementProcess):
    def __init__(self, cluster_block):
        super().__init__(process_func, Conf(), cluster_block)


def process_func(sp_result_list: Iterable[Spectrum], conf: Conf):
    sw_list = []
    control_s_radius = None
    control_w_radius = None
    for sp, _ in sp_result_list:
        sum_ys = np.sum(sp.y)
        
        center_i = np.argmax(sp.y)
        center = sp.x[center_i]

        if conf.a_radius is not None:
            a_radius = conf.a_radius
            a_range = center - a_radius, center + a_radius
            a_range_i = sp.index(a_range)
        else:
            a_range_i = 0, len(sp)
        
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
        w1, w1_var = rate_var(sp.y, sp.var, a_range_i[0], w_range_i[0])
        w2, w2_var = rate_var(sp.y, sp.var, w_range_i[1], a_range_i[1])
        w, w_var = add_var(w1, w1_var, w2, w2_var)

        sw_list.append((
            (s, s_var, s_range_i),
            (w, w_var, w_range_i),
            (w1, w1_var, (0, w_range_i[0])),
            (w2, w2_var, (w_range_i[0], len(sp))),
        ))
    return tuple(sw_list)


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
