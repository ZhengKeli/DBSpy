from spector import artifact_sw
from . import spectrum_dbs


# define

class Conf:
    def __init__(self, spectrum_conf_list, spectrum_tag_list, artifact_conf_list):
        self.spectrum_conf_list = spectrum_conf_list
        self.spectrum_tag_list = spectrum_tag_list
        self.artifact_conf_list = artifact_conf_list


class Result:
    def __init__(self, artifact_list):
        self.artifacts_list = artifact_list


class Context:
    def __init__(self):
        self.spectrum_context_list = []
        self.artifact_result_list = []


# dispatch

def process(conf: Conf, context: Context = None):
    spectrum_result_list = []
    for spectrum_conf in conf.spectrum_conf_list:
        if isinstance(spectrum_conf, spectrum_dbs.Conf):
            if context is not None:
                spectrum_context = spectrum_dbs.Context()
                context.spectrum_context_list.append(spectrum_context)
                spectrum_result = spectrum_dbs.process(spectrum_conf, spectrum_context)
            else:
                spectrum_result = spectrum_dbs.process(spectrum_conf)
        else:
            raise RuntimeError(f"Unsupported spectrum type {type(conf)}")
        spectrum_result_list.append(spectrum_result)

    artifact_result_list = []
    for artifact_conf in conf.artifact_conf_list:
        if isinstance(artifact_conf, artifact_sw.Conf):
            spectrum_list = (spectrum_result.sp_spectrum for spectrum_result in spectrum_result_list)
            artifact_result = artifact_sw.process(spectrum_list, artifact_conf)
            if context is not None:
                context.artifact_result_list.append(artifact_result)
            artifact_result_list.append(artifact_result)

    return artifact_result_list
