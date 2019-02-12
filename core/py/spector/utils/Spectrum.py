from typing import Iterable

from spector.utils.indexing import index_nearest


class Spectrum:
    def __init__(self, x, y, var=None):
        self.x = x
        self.y = y
        self.var = var
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            new_var = None if self.var is None else self.var[key]
            return Spectrum(self.x[key], self.y[key], new_var)
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
        if self.spectrum.var is not None:
            return self.spectrum.var[self.index]
        else:
            return None
