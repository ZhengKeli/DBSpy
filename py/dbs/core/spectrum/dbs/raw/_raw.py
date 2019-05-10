import numpy as np

from dbs.core import base
from dbs.utils.spectrum import Spectrum
from dbs.utils.variance import spectrum_var


# define

class Conf(base.ElementConf):
    def __init__(self, file_path=None, file_type=None):
        self.file_path = file_path
        self.file_type = file_type


class Process(base.ElementProcess):
    def __init__(self):
        super().__init__(process_func, Conf())


def process_func(conf: Conf) -> Spectrum:
    if conf.file_path is not None:
        file_path = conf.file_path
        file_type = conf.file_type
        if file_type == 'txt' or file_type is None:
            raw_x, raw_y = load_dbs_spectrum_from_txt(file_path)
        else:
            raise TypeError(f"Unsupported file type \"{file_type}\"")
    else:
        raise TypeError("Not provided any source of spectrum.")
    raw_var = spectrum_var(raw_y)
    return Spectrum(raw_x, raw_y, raw_var)


# utils

def load_dbs_spectrum_from_txt(file_path):
    m = np.loadtxt(file_path)
    return m[:, 0], m[:, 1]
