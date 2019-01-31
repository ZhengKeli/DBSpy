import matplotlib.pyplot as plt
import numpy as np

import spector

conf = spector.Conf(
    spectrum_conf_list=[spector.spectrum_dbs.Conf(
        source_conf=spector.spectrum_dbs.source.Conf(
            file_path="C:/Users/keli/OneDrive/ZKL/Develop/Projects/PositronSpector/core/data/0 ppm_#2_150523_1/energy_smoothed.txt"
        ),
        res_conf=spector.spectrum_dbs.res.Conf(
            search_center=1157,
            search_radius=5
        ),
        peak_conf=spector.spectrum_dbs.peak.Conf(
            search_center=510,
            search_radius=5,
            peak_radius=28
        ),
        bg_conf=spector.spectrum_dbs.bg.Conf(
            bg_expand=1
        )
    )],
    artifact_conf_list=[]
)
context = spector.Context()
try:
    spector.process(conf, context)
except Exception as e:
    raise e

for spectrum_context in context.spectrum_context_list:
    if isinstance(spectrum_context, spector.spectrum_dbs.Context):
        raw_spectrum = spectrum_context.source_result.raw_spectrum
        print("raw spectrum")
        plt.plot(raw_spectrum.x, raw_spectrum.y)
        plt.show()
        
        resolution = spectrum_context.res_result.resolution
        print("peak resolution", resolution)
        
        peak_spectrum = spectrum_context.peak_result.peak_spectrum
        peak_center = raw_spectrum.x[spectrum_context.peak_result.peak_center_i]
        print("peak spectrum")
        # plt.plot(raw_spectrum.x, raw_spectrum.y)
        plt.semilogy(peak_spectrum.x, peak_spectrum.y)
        plt.semilogy((peak_center, peak_center), (0, 1.3 * np.max(peak_spectrum.y)), '--')
        plt.show()
        
        bg_spectrum = spectrum_context.bg_result.bg_spectrum
        print("bg spectrum")
        plt.semilogy(peak_spectrum.x, peak_spectrum.y)
        plt.semilogy(bg_spectrum.x, bg_spectrum.y)
        plt.show()
        
        sp_spectrum = spectrum_context.sp_result.sp_spectrum
        print("sp spectrum")
        plt.semilogy(sp_spectrum.x, sp_spectrum.y)
        plt.show()

for artifact_context in context.artifact_context_list:
    print("artifact")
    # todo show artifact
