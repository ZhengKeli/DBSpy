from dbspy.core import base
from dbspy.core.spectrum import _spectrum as spectrum
from . import raw, peak, sp


# define
class Conf(spectrum.Conf):
    def __init__(self, raw_conf=None, peak_conf=None, sp_conf=None):
        self.raw = raw_conf
        self.peak = peak_conf
        self.sp = sp_conf
    
    @staticmethod
    def create_process():
        return Process()
    
    def encode_content(self):
        return {
            'raw': self.raw.encode(),
            'peak': self.peak.encode(),
            'sp': self.sp.encode()}
    
    @classmethod
    def decode_content(cls, code):
        return cls(
            raw.Conf.decode(code['raw']),
            peak.Conf.decode(code['peak']),
            sp.Conf.decode(code['sp']))


class Process(base.Process):
    def __init__(self):
        self.raw_process = raw.Process()
        self.peak_process = peak.Process(self.raw_process)
        self.sp_process = sp.Process(self.peak_process)
        super().__init__(self.sp_process.block)
    
    @property
    def conf(self) -> Conf:
        return Conf(self.raw_process.conf, self.peak_process.conf, self.sp_process.conf)
    
    @conf.setter
    def conf(self, conf: Conf):
        self.raw_process.conf = conf.raw
        self.peak_process.conf = conf.peak
        self.sp_process.conf = conf.sp
