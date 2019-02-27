from spector import artifact_sw, artifact_ratio
from . import spectrum_dbs
from .utils import BaseProcess


# define

class Conf:
    def __init__(self, spectrum_conf_list, spectrum_tag_list, artifact_conf_list):
        self.spectrum_conf_list = spectrum_conf_list
        self.spectrum_tag_list = spectrum_tag_list
        self.artifact_conf_list = artifact_conf_list


class Process(BaseProcess):
    
    def __init__(self, spectrum_process_list, artifact_process_list):
        super().__init__()
        self.spectrum_process_list = spectrum_process_list
        self.artifact_process_list = artifact_process_list
    
    @staticmethod
    def from_conf(conf: Conf):
        spectrum_process_list = []
        for spectrum_conf in conf.spectrum_conf_list:
            if isinstance(spectrum_conf, spectrum_dbs.Conf):
                spectrum_process_list.append(spectrum_dbs.Process(spectrum_conf))
            else:
                raise TypeError(f"Unsupported spectrum_conf {spectrum_conf}")
        
        artifact_process_list = []
        for artifact_conf in conf.artifact_conf_list:
            if isinstance(artifact_conf, artifact_sw.Conf):
                artifact_process_list.append(artifact_sw.Process(artifact_conf))
            elif isinstance(artifact_conf, artifact_ratio.Conf):
                artifact_process_list.append(artifact_ratio.Process(artifact_conf))
            else:
                raise TypeError(f"Unsupported artifact_conf {artifact_conf}")
        
        return Process(spectrum_process_list, artifact_process_list)
    
    def on_process(self):
        spectrum_result_list = tuple(spectrum_process.process() for spectrum_process in self.spectrum_process_list)
        spectrum_list = tuple(spectrum_result.sp_spectrum for spectrum_result in spectrum_result_list)
        artifact_result_list = tuple(artifact_process.process(spectrum_list) for artifact_process in self.artifact_process_list)
        return artifact_result_list
