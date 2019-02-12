import numpy as np

from spector.utils.Spectrum import Spectrum
from spector.utils.variance import add_var, minus_var, divide_var


# define

class Conf:
    def __init__(self, fold_mode: str = None, compare_mode: str = None):
        self.fold_mode = fold_mode
        self.compare_mode = compare_mode


class Result:
    def __init__(self, ratio_sp_list):
        self.ratio_sp_list = ratio_sp_list


# process

def process(sp_list, conf: Conf):
    sp_list, center_i = align_peak(sp_list)
    sp_fold_list = fold_sp(sp_list, center_i, conf.fold_mode)
    ys_list = tuple(sp_fold.y for sp_fold in sp_fold_list)
    ys_var_list = tuple(sp_fold.var for sp_fold in sp_fold_list)
    ratio_list, ratio_var_list = compute_ratio(ys_list, ys_var_list, conf.compare_mode)
    ratio_sp_list = tuple(Spectrum(sp_fold_list[i].x, ratio_list[i], ratio_var_list[i]) for i in range(len(sp_list)))
    return Result(ratio_sp_list)


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
        left_list = []
        for sp in sp_list:
            center = sp.x[center_i]
            left_sp = sp[:center_i + 1]
            left_sp = Spectrum(np.flip(center - left_sp.x), np.flip(left_sp.y), np.flip(left_sp.var))
            left_list.append(left_sp)
        return left_list
    elif mode == 'right':
        left_list = []
        for sp in sp_list:
            center = sp.x[center_i]
            left_sp = sp[center_i:]
            left_sp = Spectrum(left_sp.x - center, left_sp.y, left_sp.var)
            left_list.append(left_sp)
        return left_list
    elif mode == 'fold':
        sp_left_list = fold_sp(sp_list, center_i, 'left')
        sp_right_list = fold_sp(sp_list, center_i, 'right')
        len_min = min(len(sp_left_list[0]), len(sp_right_list[0]))
        fold_list = []
        for i in range(len(sp_list)):
            sp_left = sp_left_list[i][:len_min]
            sp_right = sp_right_list[i][:len_min]
            ys, ys_var = add_var(sp_left.y, sp_left.var, sp_right.y, sp_right.var)
            fold_list.append(Spectrum(sp_right.x, ys, ys_var))
        return fold_list
    else:
        raise TypeError("Unsupported fold mode")


def compute_ratio(ys_list, ys_var_list, compare_mode, control_ys=None, control_ys_var=None):
    scale_list = tuple(np.sum(ys) for ys in ys_list)
    ys_list = tuple(ys_list[i] / scale_list[i] for i in range(len(ys_list)))
    ys_var_list = tuple(ys_var_list[i] / np.square(scale_list[i]) for i in range(len(ys_var_list)))
    
    if control_ys is None:
        control_ys = ys_list[0]
    
    if control_ys_var is None:
        control_ys_var = ys_var_list[0]
    
    ratio_list = []
    ratio_var_list = []
    for i in range(len(ys_list)):
        ys = ys_list[i]
        ys_var = ys_var_list[i]
        if compare_mode == 'subtract' or compare_mode is None:
            ratio, ratio_var = minus_var(ys, ys_var, control_ys, control_ys_var)
        elif compare_mode == 'divide':
            ratio, ratio_var = divide_var(ys, ys_var, control_ys, control_ys_var)
        else:
            raise TypeError(f"Unsupported compare mode {compare_mode}")
        ratio_list.append(ratio)
        ratio_var_list.append(ratio_var)
    return ratio_list, ratio_var_list
