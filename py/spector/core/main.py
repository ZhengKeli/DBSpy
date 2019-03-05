from spector.core.base import BaseProcess
from . import spectrum, artifact


class MainConf:
    def __init__(self, spectrum_conf_list, spectrum_tag_list, artifact_conf_list):
        self.spectrum_conf_list = spectrum_conf_list
        self.spectrum_tag_list = spectrum_tag_list
        self.artifact_conf_list = artifact_conf_list

    def apply(self, process=None):
        if process is None:
            process = MainProcess()
    
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


class MainProcess(BaseProcess):
    
    def __init__(self, spectrum_process_list=None, artifact_process_list=None):
        super().__init__()
        self.spectrum_process_list = [] if spectrum_process_list is None else list(spectrum_process_list)
        self.artifact_process_list = [] if artifact_process_list is None else list(artifact_process_list)
    
    def on_process(self):
        spectrum_result_list = tuple(spectrum_process.process() for spectrum_process in self.spectrum_process_list)
        spectrum_list = tuple(spectrum_result.sp_spectrum for spectrum_result in spectrum_result_list)
        artifact_result_list = tuple(artifact_process.process(spectrum_list) for artifact_process in self.artifact_process_list)
        return artifact_result_list
