from dbspy.core import base, spectrum, analyze
from dbspy.utils.block import ClusterBlock


class Conf(base.Conf):
    def __init__(self, spectrum_confs, analyze_confs):
        self.spectrum_confs = spectrum_confs
        self.analyze_confs = analyze_confs
    
    def encode(self):
        return {
            'spectrum_confs': tuple(conf.encode() for conf in self.spectrum_confs),
            'analyze_confs': tuple(conf.encode() for conf in self.analyze_confs)}
    
    @classmethod
    def decode(cls, code: dict):
        return cls(
            tuple(spectrum.Conf.decode(c) for c in code['spectrum_confs']),
            tuple(analyze.Conf.decode(c) for c in code['analyze_confs']))


class Process(base.Process):
    def __init__(self):
        self._spectrum_processes = tuple()
        self._analyze_processes = tuple()
        self._spectrum_cluster_block = ClusterBlock()
        self._analyze_cluster_block = ClusterBlock()
        super().__init__(self._analyze_cluster_block)
    
    @property
    def spectrum_processes(self):
        return self._spectrum_processes
    
    @spectrum_processes.setter
    def spectrum_processes(self, spectrum_processes):
        self._spectrum_processes = tuple(spectrum_processes)
        self._spectrum_cluster_block.blocks = tuple(process.block for process in spectrum_processes)
    
    def append_spectrum_process(self, spectrum_process):
        spectrum_processes = list(self.spectrum_processes)
        spectrum_processes.append(spectrum_process)
        self.spectrum_processes = spectrum_processes
    
    def remove_spectrum_process(self, spectrum_process):
        spectrum_processes = list(self.spectrum_processes)
        spectrum_processes.remove(spectrum_process)
        self.spectrum_processes = spectrum_processes
    
    @property
    def analyze_processes(self):
        return self._analyze_processes
    
    @analyze_processes.setter
    def analyze_processes(self, analyze_processes):
        self._analyze_processes = tuple(analyze_processes)
        self._analyze_cluster_block.blocks = tuple(process.block for process in analyze_processes)
    
    def append_analyze_process(self, analyze_process):
        analyze_processes = list(self.analyze_processes)
        analyze_processes.append(analyze_process)
        self.analyze_processes = analyze_processes
    
    def remove_analyze_process(self, analyze_process):
        analyze_processes = list(self.analyze_processes)
        analyze_processes.remove(analyze_process)
        self.analyze_processes = analyze_processes
    
    @property
    def spectrum_cluster_block(self):
        return self._spectrum_cluster_block
    
    @property
    def analyze_cluster_block(self):
        return self._analyze_cluster_block
    
    @property
    def conf(self):
        return Conf(
            tuple(process.conf for process in self.spectrum_processes),
            tuple(process.conf for process in self.analyze_processes))
    
    @conf.setter
    def conf(self, conf: Conf):
        self.spectrum_processes = [
            conf.create_and_apply()
            for conf in conf.spectrum_confs]
        self.analyze_processes = [
            conf.create_and_apply(self.spectrum_cluster_block)
            for conf in conf.analyze_confs]
