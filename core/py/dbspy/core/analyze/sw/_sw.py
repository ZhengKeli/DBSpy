import numpy as np

from dbspy.core import base
from dbspy.core.analyze import _analyze as analyze
from dbspy.utils.indexing import search_nearest, index_nearest
from dbspy.utils.neighborhood import neighborhood
from dbspy.utils.variance import add_var, sum_var, divide_var


# define

class Conf(analyze.Conf):
    def __init__(self, s_radius=None, w_radius=None, a_radius=None, w_mode=None, tags=None):
        self.s_radius = s_radius
        self.w_radius = w_radius
        self.a_radius = a_radius
        self.w_mode = w_mode
        self.tags = tags
    
    @staticmethod
    def create_process(cluster_block):
        return Process(cluster_block)


class Process(base.ElementProcess):
    def __init__(self, cluster_block):
        super().__init__(process_func, Conf(), cluster_block)


def process_func(sp_result_list, conf: Conf):
    sw_list = []
    for (x, y, var), _ in sp_result_list:
        center_i = np.argmax(y)
        center = x[center_i]
        
        s_range_i = index_nearest(neighborhood(center, conf.s_radius), x)
        w_range_i = index_nearest(neighborhood(center, conf.w_radius), x)
        a_range_i = (0, len(x)) if conf.a_radius is None \
            else index_nearest(neighborhood(center, conf.a_radius), x)
        
        s, s_var = rate_var(y, var, *s_range_i)
        w, w_var, w_range_i = compute_w(y, var, w_range_i, a_range_i, conf.w_mode)
        sw_list.append(((s, s_var, s_range_i), (w, w_var, w_range_i)))
    return tuple((ss, ww, tag) for (ss, ww), tag in zip(sw_list, conf.tags))


# utils

def compute_w(y, var, w_range_i, a_range_i, w_mode):
    if w_mode == 'left':
        wl_range_i = a_range_i[0], w_range_i[0]
        wl, wl_var = rate_var(y, var, *wl_range_i)
        return wl, wl_var, wl_range_i
    elif w_mode == 'right':
        wr_range_i = w_range_i[1], a_range_i[1]
        wr, wr_var = rate_var(y, var, *wr_range_i)
        return wr, wr_var, wr_range_i
    elif w_mode == 'all' or w_mode is None:
        wl, wl_var, wl_range_i = compute_w(y, var, w_range_i, a_range_i, 'left')
        wr, wr_var, wr_range_i = compute_w(y, var, w_range_i, a_range_i, 'right')
        w, w_var = add_var(wl, wl_var, wr, wr_var)
        return w, w_var, (wl_range_i, wr_range_i)
    else:
        raise TypeError("Unsupported w_mode: " + w_mode)


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
