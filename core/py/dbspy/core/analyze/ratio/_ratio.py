import numpy as np

from dbspy.core import base
from dbspy.core.analyze import _analyze as analyze
from dbspy.utils.variance import add_var, minus_var, divide_var, times_var, sum_var


# define

class Conf(analyze.Conf):
    def __init__(self, fold_mode: str = None, compare_mode: str = None):
        self.fold_mode = fold_mode
        self.compare_mode = compare_mode
    
    @staticmethod
    def create_process(cluster_block):
        return Process(cluster_block)


class Process(base.ElementProcess):
    def __init__(self, cluster_block):
        super().__init__(process_func, Conf(), cluster_block)


def process_func(sp_result_list, conf: Conf):
    sp_list = tuple(np.transpose(sp) for sp, _ in sp_result_list)
    sp_list, center_i = align_peak(sp_list)
    sp_list = tuple(fold_sp(sp, center_i, conf.fold_mode) for sp in sp_list)
    ys_list, ys_var_list = zip(*((sp_fold[:, 1], sp_fold[:, 2]) for sp_fold in sp_list))
    ys_list, ys_var_list = normalize(ys_list, ys_var_list)
    ratio_list, ratio_var_list = compute_ratio(ys_list, ys_var_list, conf.compare_mode)
    ratio_sp_list = tuple(
        (sp[:, 0], ratio, ratio_var)
        for sp, ratio, ratio_var in zip(sp_list, ratio_list, ratio_var_list))
    return ratio_sp_list


# utils

def align_peak(sp_list):
    center_i_list = tuple(np.argmax(sp[:, 1]) for sp in sp_list)
    center_i_min = min(center_i_list)
    sp_list = tuple(sp_list[i][center_i_list[i] - center_i_min:] for i in range(len(sp_list)))
    
    len_list = tuple(len(sp) for sp in sp_list)
    len_min = min(len_list)
    sp_list = tuple(sp[:len_min] for sp in sp_list)
    
    return sp_list, center_i_min


def fold_sp(sp, center_i, mode):
    if mode == 'none' or mode is None:
        return sp
    elif mode == 'left':
        center = sp[center_i, 0]
        sp_left = np.copy(sp[:center_i + 1])
        sp_left[:, 0] = center - sp_left[:, 0]
        return np.flip(sp_left)
    elif mode == 'right':
        center = sp[center_i, 0]
        sp_right = np.copy(sp[center_i:])
        sp_right[:, 0] -= center
        return sp_right
    elif mode == 'fold':
        sp_left = fold_sp(sp, center_i, 'left')
        sp_right = fold_sp(sp, center_i, 'right')
        len_min = min(len(sp_left), len(sp_right))
        sp_left = sp_left[:len_min]
        sp_right = sp_right[:len_min]
        ys, ys_var = add_var(sp_left[:, 1], sp_left[:, 2], sp_right[:, 1], sp_right[:, 2])
        return np.transpose((sp_right[:, 0], ys, ys_var))
    else:
        raise TypeError("Unsupported fold mode")


def normalize(ys_list, ys_var_list, control_ys=None, control_ys_var=None):
    control_ys = ys_list[0] if control_ys is None else control_ys
    control_ys_var = ys_var_list[0] if control_ys_var is None else control_ys_var
    control_sum, control_sum_var = sum_var(control_ys, control_ys_var)
    norm_ys_list, norm_ys_var_list = [], []
    for ys, ys_var in zip(ys_list, ys_var_list):
        ys_sum, ys_sum_var = sum_var(ys, ys_var)
        scale, scale_var = divide_var(control_sum, control_sum_var, ys_sum, ys_sum_var)
        norm_ys, norm_ys_var = times_var(ys, ys_var, scale, scale_var)
        norm_ys_list.append(norm_ys)
        norm_ys_var_list.append(norm_ys_var)
    return norm_ys_list, norm_ys_var_list


def compute_ratio(ys_list, ys_var_list, compare_mode, control_ys=None, control_ys_var=None):
    control_ys = ys_list[0] if control_ys is None else control_ys
    control_ys_var = ys_var_list[0] if control_ys_var is None else control_ys_var
    ratio_list, ratio_var_list = [], []
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
