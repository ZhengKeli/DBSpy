from .indexing import index_nearest


class Spectrum:
    def __init__(self, x, y, var=None):
        self.x = x
        self.y = y
        self.var = var
        self.slice = 0
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return SpectrumPoint(self, key)
        elif isinstance(key, slice):
            new_var = None if self.var is None else self.var[key]
            return Spectrum(self.x[key], self.y[key], new_var)
        else:
            raise TypeError(f'Unsupported key {key}')
    
    def index(self, x):
        if isinstance(self.x, ChannelSet):
            i1 = int((x - self.x.start) / self.x.step)
            i2 = i1 + 1
            if (x - self.x[i1] < self.x[i2] - x) == self.x.step > 0:
                return i1
            else:
                return i2
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


class ChannelSet:
    def __init__(self, start, step, count):
        self.start = start
        self.step = step
        self.count = count
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.start + self.step * key
        elif isinstance(key, slice):
            slice_start = 0 if key.start is None else key.start
            slice_stop = self.count if key.start is None else key.stop
            slice_step = 1 if key.step is None else key.step
            return ChannelSet(self[slice_start], self.step * slice_step, int((slice_stop - slice_start) / slice_step))
    
    def __len__(self):
        return self.count
