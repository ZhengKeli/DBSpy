import numpy as np

# define
from spector.utils.spectrum import Spectrum
from spector.utils.variance import add_var, minus_var, divide_var


class Conf:
    def __init__(self, fold_mode: str = None, compare_mode: str = None):
        self.fold_mode = fold_mode
        self.compare_mode = compare_mode


class Result:
    def __init__(self, ratio_list, ratio_var_list):
        self.ratio_list = ratio_list
        self.ratio_var_list = ratio_var_list


# process

def process(sp_list, conf: Conf):
    sp_list, center_i = align_peak(sp_list)
    sp_fold_list = fold_sp(sp_list, center_i, conf.fold_mode)
    
    control_sp = sp_fold_list[0]
    ratio_list = []
    ratio_var_list = []
    for sp_fold in sp_fold_list:
        if conf.compare_mode == 'subtract' or conf.compare_mode is None:
            ratio, ratio_var = minus_var(sp_fold.y, sp_fold.var, control_sp.y, control_sp.var)
        elif conf.compare_mode == 'divide':
            ratio, ratio_var = divide_var(sp_fold.y, sp_fold.var, control_sp.y, control_sp.var)
        else:
            raise TypeError(f"Unsupported compare mode {conf.compare_mode}")
        ratio_list.append(ratio)
        ratio_var_list.append(ratio_var)
    return Result(ratio_list, ratio_var_list)


# utils

def align_peak(sp_list):
    center_i_list = tuple(np.argmax(sp.y) for sp in sp_list)
    center_i_min = min(center_i_list)
    sp_list = tuple(sp_list[i][center_i_list[i] - center_i_min:] for i in range(len(sp_list)))
    
    len_list = tuple(len(sp) for sp in sp_list)
    len_min = min(len_list)
    sp_list = tuple(sp[:len_min] for sp in sp_list)
    
    return sp_list, center_i_min


def fold_sp(sp_list, center_i, mode):
    if mode == 'none' or mode is None:
        return sp_list
    elif mode == 'left':
        return tuple(sp[:center_i + 1] for sp in sp_list)
    elif mode == 'right':
        return tuple(sp[center_i:] for sp in sp_list)
    elif mode == 'fold':
        sp_left_list = fold_sp(sp_list, center_i, 'left')
        sp_right_list = fold_sp(sp_list, center_i, 'right')
        len_min = min(len(sp_left_list[0]), len(sp_right_list[0]))
        fold_list = []
        for i in range(len(sp_list)):
            sp_left = sp_left_list[i][:len_min]
            sp_right = sp_right_list[i][:len_min]
            ys, ys_var = add_var(np.flip(sp_left.y, 0), np.flip(sp_left.var, 0), sp_right.y, sp_right.var)
            ys = ys / 2
            ys_var = ys_var / 2
            fold_list.append(Spectrum(sp_right.x, ys, ys_var))
        return fold_list
    else:
        raise TypeError("Unsupported fold mode")
