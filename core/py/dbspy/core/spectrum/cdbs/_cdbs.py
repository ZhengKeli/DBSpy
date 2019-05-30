from dbspy.core.spectrum import _spectrum as spectrum
from . import raw, peak, sp


# define
class Conf(spectrum.Conf):
    def __init__(self, tag=None, raw_conf=None, peak_conf=None, sp_conf=None):
        super().__init__(tag)
        self.raw = raw_conf
        self.peak = peak_conf
        self.sp = sp_conf
    
    def create_process(self):
        return Process(self.tag)
    
    def encode_content(self):
        return {
            'raw': self.raw.encode(),
            'peak': self.peak.encode(),
            'sp': self.sp.encode()}
    
    @classmethod
    def decode_content(cls, code):
        return cls(raw.Conf.decode(code['raw']), peak.Conf.decode(code['peak']), sp.Conf.decode(code['sp']))


class Process(spectrum.Process):
    def __init__(self, tag):
        self.raw_process = raw.Process()
        self.peak_process = peak.Process(self.raw_process)
        self.sp_process = sp.Process(self.peak_process)
        super().__init__(self.sp_process.block, tag)
    
    @property
    def conf(self) -> Conf:
        return Conf(
            self.tag,
            self.raw_process.conf,
            self.peak_process.conf,
            self.sp_process.conf)
    
    @conf.setter
    def conf(self, conf: Conf):
        self.tag = conf.tag
        self.raw_process.conf = conf.raw
        self.peak_process.conf = conf.peak
        self.sp_process.conf = conf.sp
