import numpy as np
from scipy import ndimage

from dbspy.core import base
# define
from dbspy.utils.indexing import index_nearest
from dbspy.utils.neighborhood import neighborhood
from dbspy.utils.variance import spectrum_var


class Conf(base.ElementConf):
    def __init__(self, search_range_xd=neighborhood(0, 5),
                 search_range_xm=neighborhood(0, 5),
                 peak_radius_xd=35, peak_radius_xm=35):
        # todo rotate
        self.search_range_xd = search_range_xd
        self.search_range_xm = search_range_xm
        self.peak_radius_xd = peak_radius_xd
        self.peak_radius_xm = peak_radius_xm


class Process(base.ElementProcess):
    def __init__(self, raw_process):
        super().__init__(process_func, Conf(), raw_process.block)


def process_func(raw_result, conf: Conf):
    (xd, xm), y = raw_result
    y_var = spectrum_var(y)
    
    search_range_xd = (0, len(xd)) if conf.search_range_xd is None else conf.search_range_xd
    search_range_xm = (0, len(xm)) if conf.search_range_xm is None else conf.search_range_xm
    
    search_range_i = index_nearest(search_range_xd, xd)
    search_range_j = index_nearest(search_range_xm, xm)
    y_blur = ndimage.gaussian_filter(y, 3.0)
    peak_i, peak_j = search_peak_center_ij(y_blur, search_range_i, search_range_j)
    
    peak_range_xd = (0, len(xd)) if conf.peak_radius_xd is None \
        else neighborhood(xd[peak_i], conf.peak_radius_xd)
    peak_range_xm = (0, len(xm)) if conf.peak_radius_xm is None \
        else neighborhood(xm[peak_j], conf.peak_radius_xm)
    peak_range_id = index_nearest(peak_range_xd, xd)
    peak_range_im = index_nearest(peak_range_xm, xm)
    
    xd = xd[slice(*peak_range_id)]
    xm = xm[slice(*peak_range_im)]
    y = y[slice(*peak_range_id), slice(*peak_range_im)]
    y_var = y_var[slice(*peak_range_id), slice(*peak_range_im)]
    peak_id = peak_i - peak_range_id[0]
    peak_im = peak_j - peak_range_im[0]
    
    return (peak_range_id, peak_range_im), ((xd, xm), y, y_var), (peak_id, peak_im)


# utils

def search_peak_center_ij(y, search_range_i, search_range_j):
    y = y[slice(*search_range_i), slice(*search_range_j)]
    i, j = np.unravel_index(np.argmax(y), np.shape(y))
    i += search_range_i[0]
    j += search_range_j[0]
    return i, j
