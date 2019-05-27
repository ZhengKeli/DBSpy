from dbspy.core import base, spectrum, artifact
from dbspy.utils.block import ClusterBlock


class Conf(base.Conf):
    def __init__(self, spectrum_confs, artifact_confs):
        self.spectrum_confs = spectrum_confs
        self.artifact_confs = artifact_confs
    
    def encode(self):
        return {
            'spectrum_cluster': tuple(conf.encode() for conf in self.spectrum_confs),
            'artifact_cluster': tuple(conf.encode() for conf in self.artifact_confs)}
    
    @classmethod
    def decode(cls, code: dict):
        return cls(
            tuple(spectrum.Conf.decode(c) for c in code['spectrum_cluster']),
            tuple(artifact.Conf.decode(c) for c in code['artifact_cluster']))


class Process(base.Process):
    def __init__(self):
        self._spectrum_processes = tuple()
        self._artifact_processes = tuple()
        self._spectrum_cluster_block = ClusterBlock()
        self._artifact_cluster_block = ClusterBlock()
        super().__init__(self._artifact_cluster_block)
    
    @property
    def spectrum_processes(self):
        return self._spectrum_processes
    
    @spectrum_processes.setter
    def spectrum_processes(self, spectrum_processes):
        self._spectrum_processes = tuple(spectrum_processes)
        self._spectrum_cluster_block.blocks = tuple(process.block for process in spectrum_processes)
    
    @property
    def artifact_processes(self):
        return self._artifact_processes
    
    @artifact_processes.setter
    def artifact_processes(self, artifact_processes):
        self._artifact_processes = tuple(artifact_processes)
        self._artifact_cluster_block.blocks = tuple(process.block for process in artifact_processes)
    
    @property
    def spectrum_cluster_block(self):
        return self._spectrum_cluster_block
    
    @property
    def artifact_cluster_block(self):
        return self._artifact_cluster_block
    
    @property
    def conf(self):
        return Conf(
            tuple(process.conf for process in self.spectrum_processes),
            tuple(process.conf for process in self.artifact_processes))
    
    @conf.setter
    def conf(self, conf: Conf):
        self.spectrum_processes = [
            conf.create_and_apply()
            for conf in conf.spectrum_confs]
        self.artifact_processes = [
            conf.create_and_apply(self.spectrum_cluster_block)
            for conf in conf.artifact_confs]
