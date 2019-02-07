import matplotlib.pyplot as plt

import spector

conf = spector.Conf(
    spectrum_conf_list=[spector.spectrum_dbs.Conf(
        source_conf=spector.spectrum_dbs.source.Conf(
            file_path=file_path
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
    ) for file_path in [
        "C:/Users/keli/OneDrive/Develop/Projects/PositronSpector/core/data/0 ppm__1_150218/energy_smoothed.txt",
        "C:/Users/keli/OneDrive/Develop/Projects/PositronSpector/core/data/80 ppm_#4_150515/energy_smoothed.txt",
        "C:/Users/keli/OneDrive/Develop/Projects/PositronSpector/core/data/150 ppm_#5_150515_1/energy_smoothed.txt",
        "C:/Users/keli/OneDrive/Develop/Projects/PositronSpector/core/data/230 ppm_#8_150516/energy_smoothed.txt",
        "C:/Users/keli/OneDrive/Develop/Projects/PositronSpector/core/data/310 ppm_#9_150516_1/energy_smoothed.txt",
        "C:/Users/keli/OneDrive/Develop/Projects/PositronSpector/core/data/610 ppm_#6_150519/energy_smoothed.txt",
    ]],
    spectrum_tag_list=[0, 80, 150, 230, 310, 610],
    artifact_conf_list=[
        spector.artifact_sw.Conf(
            control_s=0.5,
            control_w=0.03
        ),
        spector.artifact_ratio.Conf(
            fold_mode='fold',
            compare_mode='subtract'
        )
    ]
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
        # plt.plot(raw_spectrum.x, raw_spectrum.y)
        # plt.show()
        
        resolution = spectrum_context.res_result.resolution
        print("peak resolution", resolution)
        
        peak_spectrum = spectrum_context.peak_result.peak_spectrum
        peak_center = raw_spectrum.x[spectrum_context.peak_result.peak_center_i]
        print("peak spectrum")
        # plt.plot(raw_spectrum.x, raw_spectrum.y)
        # plt.semilogy(peak_spectrum.x, peak_spectrum.y)
        # plt.semilogy((peak_center, peak_center), (0, 1.3 * np.max(peak_spectrum.y)), '--')
        # plt.show()
        
        bg_spectrum = spectrum_context.bg_result.bg_spectrum
        print("bg spectrum")
        # plt.semilogy(peak_spectrum.x, peak_spectrum.y)
        # plt.semilogy(bg_spectrum.x, bg_spectrum.y)
        # plt.show()
        
        sp_spectrum = spectrum_context.sp_result.sp_spectrum
        print("sp spectrum")
        # plt.semilogy(sp_spectrum.x, sp_spectrum.y)
        # plt.show()

for artifact_result in context.artifact_result_list:
    if isinstance(artifact_result, spector.artifact_sw.Result):
        print("s curve")
        s_list = tuple([sw_result.s for sw_result in artifact_result.result_list])
        s_var_list = tuple([sw_result.s_var for sw_result in artifact_result.result_list])
        # plt.plot(conf.spectrum_tag_list, s_list)
        # plt.errorbar(conf.spectrum_tag_list, s_list, np.sqrt(s_var_list), capsize=3)
        # plt.show()
        
        print("w curve")
        w_list = tuple([sw_result.w for sw_result in artifact_result.result_list])
        w_var_list = tuple([sw_result.w_var for sw_result in artifact_result.result_list])
        # plt.plot(conf.spectrum_tag_list, w_list)
        # plt.errorbar(conf.spectrum_tag_list, w_list, np.sqrt(w_var_list), capsize=3)
        # plt.show()
    elif isinstance(artifact_result, spector.artifact_ratio.Result):
        print("ratio curves")
        for ratio in artifact_result.ratio_list:
            plt.plot(range(len(ratio)), -ratio)
        plt.legend(conf.spectrum_tag_list)
        plt.show()
