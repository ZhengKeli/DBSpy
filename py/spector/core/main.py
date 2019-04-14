from spector.core.base import BaseProcess


class Process(BaseProcess):
    
    def __init__(self, spectrum_process_list=None, artifact_process_list=None):
        super().__init__()
        self.spectrum_process_list = [] if spectrum_process_list is None else list(spectrum_process_list)
        self.artifact_process_list = [] if artifact_process_list is None else list(artifact_process_list)
    
    def on_process(self):
        spectrum_result_list = tuple(spectrum_process.process() for spectrum_process in self.spectrum_process_list)
        spectrum_list = tuple(spectrum_result.sp_spectrum for spectrum_result in spectrum_result_list)
        artifact_result_list = tuple(artifact_process.process(spectrum_list) for artifact_process in self.artifact_process_list)
        return artifact_result_list
