import numpy as np

from spector.spectrum_dbs.peak import spectrum_var
from spector.utils import BaseProcess
from spector.utils.Spectrum import Spectrum


# define

class Conf:
    def __init__(self, file_path=None, file_type=None):
        self.file_path = file_path
        self.file_type = file_type


class Result:
    def __init__(self, raw_spectrum: Spectrum):
        self.raw_spectrum = raw_spectrum


class Process(BaseProcess):
    
    def __init__(self, conf: Conf):
        super().__init__()
        self.conf = conf
    
    def on_process(self):
        return process(self.conf)


# process

def process(conf: Conf) -> Result:
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
    return Result(Spectrum(raw_x, raw_y, raw_var))


# execute

def load_dbs_spectrum_from_txt(file_path):
    m = np.loadtxt(file_path)
    return m[:, 0], m[:, 1]
