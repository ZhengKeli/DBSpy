from spector import artifact_sw, artifact_ratio
from . import spectrum_dbs
from .utils import ProcessBlock


# define

class Conf:
    def __init__(self, spectrum_conf_list, spectrum_tag_list, artifact_conf_list):
        self.spectrum_conf_list = spectrum_conf_list
        self.spectrum_tag_list = spectrum_tag_list
        self.artifact_conf_list = artifact_conf_list


class Result:
    def __init__(self, artifact_list):
        self.artifacts_list = artifact_list


class SpectorBlock(ProcessBlock):
    
    def __init__(self, conf: Conf):
        super().__init__()
        self.conf = conf
        
        self.spectrum_blocks = []
        for spectrum_conf in conf.spectrum_conf_list:
            if isinstance(spectrum_conf, spectrum_dbs.Conf):
                self.spectrum_blocks.append(spectrum_dbs.DBSBlock(spectrum_conf))
            else:
                raise TypeError(f"Unsupported spectrum_conf {spectrum_conf}")
        
        self.artifact_blocks = []
        for artifact_conf in conf.artifact_conf_list:
            if isinstance(artifact_conf, artifact_sw.Conf):
                self.artifact_blocks.append(artifact_sw.SWBlock(artifact_conf))
            elif isinstance(artifact_conf, artifact_ratio.Conf):
                self.artifact_blocks.append(artifact_ratio.RatioBlock(artifact_conf))
            else:
                raise TypeError(f"Unsupported artifact_conf {artifact_conf}")
    
    def on_process(self):
        spectrum_result_list = tuple(spectrum_block.process() for spectrum_block in self.spectrum_blocks)
        spectrum_list = tuple(spectrum_result.sp_spectrum for spectrum_result in spectrum_result_list)
        
        artifact_result_list = tuple(artifact_block.process(spectrum_list) for artifact_block in self.artifact_blocks)
        
        return Result(artifact_result_list)
