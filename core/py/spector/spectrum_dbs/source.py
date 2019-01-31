import numpy as np

from spector.utils.spectrum import Spectrum


# define


class Conf:
    def __init__(self, file_path=None, file_type=None):
        self.file_path = file_path
        self.file_type = file_type


class Result:
    def __init__(self, raw_spectrum: Spectrum):
        self.raw_spectrum = raw_spectrum


# dispatch

def process(conf: Conf) -> Result:
    if conf.file_path is not None:
        file_path = conf.file_path
        file_type = conf.file_type
        if file_type == 'txt' or file_type is None:
            raw_spectrum = load_dbs_spectrum_from_txt(file_path)
        else:
            raise TypeError(f"Unsupported file type \"{file_type}\"")
    else:
        raise TypeError("Not provided any source of spectrum.")
    
    return Result(raw_spectrum)


# execute

def load_dbs_spectrum_from_txt(file_path) -> Spectrum:
    m = np.loadtxt(file_path)
    xs = m[:, 0]
    ys = m[:, 1]
    # channels = ChannelSet(xs[0], xs[1] - xs[0], len(xs))
    return Spectrum(xs, ys)
