from spector import conf
from spector import core
from spector.app import Application

if __name__ == '__main__':
    main_conf = conf.main.Conf(
        spectrum_conf_list=[core.spectrum.dbs.Conf(
            raw_conf=core.spectrum.dbs.raw.Conf(
                file_path=file_path
            ),
            res_conf=core.spectrum.dbs.res.Conf(
                search_center=1157,
                search_radius=5
            ),
            peak_conf=core.spectrum.dbs.peak.Conf(
                search_center=510,
                search_radius=5,
                peak_radius=28
            ),
            bg_conf=core.spectrum.dbs.bg.Conf(
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
            core.artifact.sw.Conf(
                control_s=0.5,
                control_w=0.03
            ),
            core.artifact.ratio.Conf(
                fold_mode='fold',
                compare_mode='subtract'
            )
        ]
    )
    main_process = main_conf.apply()
    Application(main_process)
