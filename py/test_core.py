import matplotlib.pyplot as plt
import numpy as np

import spector.core as core

conf = core.main.Conf(
    spectrum_conf_list=[core.spectrum_dbs.Conf(
        raw_conf=core.spectrum_dbs.raw.Conf(
            file_path=file_path
        ),
        res_conf=core.spectrum_dbs.res.Conf(
            search_center=1157,
            search_radius=5
        ),
        peak_conf=core.spectrum_dbs.peak.Conf(
            search_center=510,
            search_radius=5,
            peak_radius=28
        ),
        bg_conf=core.spectrum_dbs.bg.Conf(
            bg_expand=1
        )
    ) for file_path in [
        "C:/Users/keli/OneDrive/Develop/Projects/PositronSpector/_materials/data/" + name + "/energy_smoothed.txt"
        for name in [
            "0 ppm__1_150218",
            "80 ppm_#4_150515",
            "150 ppm_#5_150515_1",
            "230 ppm_#8_150516",
            "310 ppm_#9_150516_1",
            "610 ppm_#6_150519"]
    ]],
    spectrum_tag_list=[0, 80, 150, 230, 310, 610],
    artifact_conf_list=[
        core.artifact_sw.Conf(
            control_s=0.5,
            control_w=0.03
        ),
        core.artifact_ratio.Conf(
            fold_mode='fold',
            compare_mode='subtract'
        )
    ]
)
main_process = core.main.Process.from_conf(conf)

main_process.process()

plt.figure(figsize=(8, 4))
plt.tight_layout()

for spectrum_process in main_process.spectrum_process_list:
    if isinstance(spectrum_process, core.spectrum_dbs.Process):
        raw_spectrum = spectrum_process.raw_process.result.raw_spectrum
        print("raw spectrum")
        # plt.plot(raw_spectrum.x, raw_spectrum.y)
        # plt.xlabel("Энергия γ-кванта, кэВ")
        # plt.ylabel("Интенсивность")
        # plt.show()
        
        if spectrum_process.res_process is not None:
            resolution = spectrum_process.res_process.result.resolution
        else:
            resolution = None
        print("peak resolution", resolution)
        
        peak_spectrum = spectrum_process.peak_process.result.peak_spectrum
        peak_center = raw_spectrum.x[spectrum_process.peak_process.result.peak_center_i]
        print("peak spectrum")
        # plt.plot(raw_spectrum.x, raw_spectrum.y)
        # plt.semilogy(peak_spectrum.x, peak_spectrum.y)
        # plt.semilogy((peak_center, peak_center), (0, 1.3 * np.max(peak_spectrum.y)), '--')
        # plt.show()
        
        bg_spectrum = spectrum_process.bg_process.result.bg_spectrum
        print("bg spectrum")
        # plt.semilogy(peak_spectrum.x, peak_spectrum.y)
        # plt.semilogy(bg_spectrum.x, bg_spectrum.y)
        # plt.legend(['исходный спектр', 'фон'])
        # plt.xlabel("Энергия γ-кванта, кэВ")
        # plt.ylabel("Интенсивность")
        # plt.show()
        
        sp_spectrum = spectrum_process.result.sp_spectrum
        print("sp spectrum")
        # plt.semilogy(sp_spectrum.x, sp_spectrum.y)
        # plt.show()

for artifact_process in main_process.artifact_process_list:
    if isinstance(artifact_process, core.artifact_sw.Process):
        print("s curve")
        s_list = tuple(sw_item.s for sw_item in artifact_process.result.items)
        s_var_list = tuple(sw_item.s_var for sw_item in artifact_process.result.items)
        plt.plot(conf.spectrum_tag_list, s_list)
        plt.errorbar(conf.spectrum_tag_list, s_list, np.sqrt(s_var_list), capsize=3)
        plt.show()
        
        print("w curve")
        w_list = tuple(sw_item.w for sw_item in artifact_process.result.items)
        w_var_list = tuple(sw_item.w_var for sw_item in artifact_process.result.items)
        # plt.plot(conf.spectrum_tag_list, w_list)
        # plt.errorbar(conf.spectrum_tag_list, w_list, np.sqrt(w_var_list), capsize=3)
        # plt.show()
    elif isinstance(artifact_process, core.artifact_ratio.Process):
        print("ratio curves")
        for ratio_sp in artifact_process.result.ratio_sp_list:
            # plt.errorbar(ratio_sp.x, ratio_sp.y, np.sqrt(ratio_sp.var), capsize=3)
            # plt.plot(ratio_sp.x, ratio_sp.y)
            pass
        # plt.legend(conf.spectrum_tag_list)
        # plt.show()
