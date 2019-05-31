import numpy as np

from dbspy.core import base
from dbspy.core.analyze import _analyze as analyze
from dbspy.utils.variance import add_var, minus_var, divide_var, sum_var


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
    sp_list = tuple(np.array(sp) for sp, _ in sp_result_list)
    x, yv_list, center_i = align_list(sp_list)
    x, yv_list = fold_list(x, yv_list, center_i, conf.fold_mode)
    yv_list = tuple(divide_var(y, y_var, *sum_var(y, y_var)) for y, y_var in yv_list)
    yv_list = compare_list(yv_list, conf.compare_mode)
    return tuple((x, y, y_var) for y, y_var in yv_list)


# utils

def align_list(sp_list, control_index=0):
    # todo recode if the x is not the same
    
    center_i_list = tuple(np.argmax(sp[1, :]) for sp in sp_list)
    center_i_min = min(center_i_list)
    sp_list = tuple(sp_list[i][:, center_i_list[i] - center_i_min:] for i in range(len(sp_list)))
    
    len_list = tuple(np.shape(sp)[1] for sp in sp_list)
    len_min = min(len_list)
    
    x = sp_list[control_index][0][:len_min]
    yv_list = tuple((y[:len_min], y_var[:len_min]) for _, y, y_var in sp_list)
    
    return x, yv_list, center_i_min


def fold_list(x, yv_list, center_i, mode):
    yv_list = np.array(yv_list)
    if mode == 'none' or mode is None:
        return x, yv_list
    elif mode == 'left':
        x_left = x[center_i] - x[:center_i + 1]
        yv_left_list = yv_list[:, :, :center_i + 1]
        return np.flip(x_left), np.flip(yv_left_list, 2)
    elif mode == 'right':
        x_right = x[center_i:] - x[center_i]
        yv_right_list = yv_list[:, :, center_i:]
        return x_right, yv_right_list
    elif mode == 'fold':
        x_left, yv_left_list = fold_list(x, yv_list, center_i, 'left')
        x_right, yv_right_list = fold_list(x, yv_list, center_i, 'right')
        len_min = min(len(x_left), len(x_right))
        
        x = x_right[:len_min]
        yv_left_list = yv_left_list[:, :, :len_min]
        yv_right_list = yv_right_list[:, :, :len_min]
        yv_list = np.transpose(add_var(
            *yv_left_list.transpose([1, 0, 2]),
            *yv_right_list.transpose([1, 0, 2])
        ), [1, 0, 2])
        return x, yv_list
    else:
        raise TypeError("Unsupported fold mode")


def compare_list(yv_list, compare_mode, control_index=0):
    control_yv = None if control_index is None else yv_list[control_index]
    return list(compare_yv(yv, control_yv, compare_mode, i == control_index) for i, yv in enumerate(yv_list))


def compare_yv(yv, control_yv, compare_mode, ignore_var=False):
    y, y_var = yv
    if compare_mode in ('difference', 'subtract', None):
        control_y, control_y_var = (0, 0) if control_yv is None else control_yv
        c, c_var = minus_var(y, y_var, control_y, control_y_var)
    elif compare_mode in ('ratio', 'divide'):
        control_y, control_y_var = (1, 0) if control_yv is None else control_yv
        c, c_var = divide_var(y, y_var, control_y, control_y_var)
    else:
        raise TypeError(f"Unsupported compare mode {compare_mode}")
    c_var = np.zeros_like(c_var) if ignore_var else c_var
    return c, c_var
