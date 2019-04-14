from spector.conf.base import BaseConf
from spector.core import *
from spector.core.base import BaseProcess


class Conf(BaseConf):
    def __init__(self, spectrum_conf_list, spectrum_tag_list, artifact_conf_list):
        self.spectrum_conf_list = spectrum_conf_list
        self.spectrum_tag_list = spectrum_tag_list
        self.artifact_conf_list = artifact_conf_list
    
    def apply(self, process=None):
        if process is None:
            process = main.Process()
        
        spectrum_process_list = []
        for spectrum_conf in self.spectrum_conf_list:
            if isinstance(spectrum_conf, spectrum.dbs.Conf):
                spectrum_process_list.append(spectrum.dbs.Process.from_conf(spectrum_conf))
            else:
                raise TypeError(f"Unsupported spectrum_conf {spectrum_conf}")
        
        artifact_process_list = []
        for artifact_conf in self.artifact_conf_list:
            if isinstance(artifact_conf, artifact.sw.Conf):
                artifact_process_list.append(artifact.sw.Process(artifact_conf))
            elif isinstance(artifact_conf, artifact.ratio.Conf):
                artifact_process_list.append(artifact.ratio.Process(artifact_conf))
            else:
                raise TypeError(f"Unsupported artifact_conf {artifact_conf}")
        
        process.spectrum_process_list = spectrum_process_list
        process.artifact_process_list = artifact_process_list
        return process
    
    @staticmethod
    def reset(process: BaseProcess):
        
        pass
    
    def encode(self):
        pass
    
    @staticmethod
    def decode(code):
        pass
