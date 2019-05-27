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
    :rtype: tuple[np.ndarray,np.ndarray]
    :return: x, y
    """
    if conf.file_path is not None:
        file_path = conf.file_path
        file_type = conf.file_type
        if file_type == 'txt' or file_type is None:
            return load_dbs_spectrum_from_txt(file_path)
        else:
            raise TypeError(f"Unsupported file type \"{file_type}\"")
    else:
        raise TypeError("Not provided any source of spectrum.")


# utils

def load_dbs_spectrum_from_txt(file_path):
    m = np.loadtxt(file_path)
    return m[:, 0], m[:, 1]
