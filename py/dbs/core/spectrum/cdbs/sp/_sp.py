import numpy as np

from dbs.core import base
from dbs.utils.gaussian import gaussian_fwhm, gaussian_fit
from dbs.utils.indexing import index_nearest
from dbs.utils.neighborhood import neighborhood
from dbs.utils.spectrum import Spectrum
from dbs.utils.variance import sum_var


# define

class Conf(base.ElementConf):
    def __init__(self, sp_band_radius=0.0, res_band_radius=0.0):
        self.sp_band_radius = sp_band_radius
        self.res_band_radius = res_band_radius


class Process(base.ElementProcess):
    def __init__(self, peak_process):
        super().__init__(process_func, Conf(), peak_process.block)


def process_func(peak_result, conf: Conf):
    ((xd, xm), y, y_var), (pd_center_i, pm_center_i) = peak_result
    
    xm_range_i = index_nearest(neighborhood(xm[pm_center_i], conf.sp_band_radius), xm)
    xm_range_i = remain_one(*xm_range_i)
    sp_y, sp_y_var = sum_var(y[:, slice(*xm_range_i)], y_var[:, slice(*xm_range_i)], 1)
    sp_x = xd
    
    xd_range_i = index_nearest(neighborhood(xd[pd_center_i], conf.res_band_radius), xd)
    xd_range_i = remain_one(*xd_range_i)
    res_y = np.mean(y[slice(*xd_range_i), :], 0)
    res_x = xm - xm[pm_center_i]
    points = np.stack((res_x, res_y), 1)
    resolution = gaussian_fwhm(gaussian_fit(points))
    
    return Spectrum(sp_x, sp_y, sp_y_var), resolution


# utils
def remain_one(s, e):
    return (s, s + 1) if not e > s else (s, e)
