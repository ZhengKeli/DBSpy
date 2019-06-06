import numpy as np
from scipy import ndimage

from dbspy.core import base
from dbspy.utils.indexing import index_nearest
from dbspy.utils.neighborhood import neighborhood
from dbspy.utils.variance import spectrum_var


# define

class Conf(base.ElementConf):
    def __init__(self, search_range=None, peak_radius=None):
        self.search_range = search_range
        self.peak_radius = peak_radius


class Process(base.ElementProcess):
    def __init__(self, raw_process):
        super().__init__(process_func, Conf(), raw_process.block)


def process_func(raw_result, conf: Conf):
    x, y = raw_result
    y_var = spectrum_var(y)
    search_range_i = (0, len(x)) if conf.search_range is None \
        else index_nearest(conf.search_range, x)
    
    y_blur = ndimage.gaussian_filter1d(y, 3.0)
    peak_center_i = search_peak_center_i(y_blur, *search_range_i)
    peak_center = x[peak_center_i]
    
    peak_range = neighborhood(peak_center, conf.peak_radius)
    peak_range_i = index_nearest(peak_range, x)
    
    peak_x = x[slice(*peak_range_i)]
    peak_y = y[slice(*peak_range_i)]
    peak_y_var = y_var[slice(*peak_range_i)]
    peak_center_i -= peak_range_i[0]
    
    return peak_range_i, (peak_x, peak_y, peak_y_var), peak_center_i


# utils

def search_peak_center_i(ys, search_head_i, search_tail_i):
    search_ys = ys[search_head_i:search_tail_i]
    peak_center_i = np.argmax(search_ys) + search_head_i
    return peak_center_i
