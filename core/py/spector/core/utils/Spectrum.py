from typing import Iterable

import numpy as np

from ..utils.indexing import index_nearest


class Spectrum:
    def __init__(self, x, y=None, var=None):
        self.x = x
        self.y = np.zeros_like(x) if y is None else y
        self.var = np.zeros_like(x) if var is None else var
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            return Spectrum(self.x[key], self.y[key], self.var[key])
        else:
            return SpectrumPoint(self, key)
    
    def __len__(self):
        return len(self.x)
    
    def index(self, x):
        if isinstance(x, Iterable):
            return tuple([self.index(xi) for xi in x])
        return index_nearest(x, self.x)


class SpectrumPoint:
    def __init__(self, spectrum: Spectrum, index: int):
        self.spectrum = spectrum
        self.index = index
    
    @property
    def x(self):
        return self.spectrum.x[self.index]
    
    @property
    def y(self):
        return self.spectrum.y[self.index]
    
    @property
    def var(self):
        return self.spectrum.var[self.index]
