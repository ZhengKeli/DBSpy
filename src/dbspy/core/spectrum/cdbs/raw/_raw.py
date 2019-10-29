import numpy as np

from dbspy.core import base


# define


class Conf(base.ElementConf):
    def __init__(self, file_path=None, file_type=None):
        self.file_path = file_path
        self.file_type = file_type


class Process(base.ElementProcess):
    def __init__(self):
        super().__init__(process_func, Conf())


def process_func(conf: Conf):
    """
    :rtype: tuple[tuple[np.ndarray,np.ndarray],np.ndarray]
    :return: (xi, xj), y
    """
    if conf.file_path is not None:
        file_path = conf.file_path
        file_type = conf.file_type
        if file_type == 'txt' or file_type is None:
            return load_from_txt(file_path)
        else:
            raise TypeError(f"Unsupported file type \"{file_type}\"")
    else:
        raise TypeError("Not provided any source of spectrum.")


# utils

def load_from_txt(file_path):
    return load_from_matrix(np.loadtxt(file_path))


def load_from_matrix(matrix):
    xi, xj, y = np.transpose(matrix)
    xi_mono, xi_period = mono(xi), period(xi)
    xj_mono, xj_period = mono(xj), period(xj)
    if xi_mono > xi_period and xj_period > xj_mono:
        xi = xi[::xi_mono]
        xj = xj[:xj_period]
        y = np.stack(np.split(y, int(len(y) / xi_mono)), 0)
    elif xi_period > xi_mono and xj_mono > xj_period:
        xi = xi[:xi_period]
        xj = xj[::xj_mono]
        y = np.array(np.split(y, int(len(y) / xj_mono)), 1)
    return (xi, xj), y


def mono(xs):
    i = 0
    for i in range(1, len(xs)):
        if xs[i] != xs[i - 1]:
            break
    return i


def period(xs):
    i = 0
    for i in range(1, len(xs)):
        if xs[i] == xs[0]:
            break
    return i
