import numpy as np
import scipy.optimize as opt

from dbspy.core import base
from dbspy.core.analyze import _analyze as analyze
from dbspy.utils.variance import add_var, minus_var, divide_var, sum_var


# define

class Conf(analyze.Conf):
    fold_modes = ('fold', 'none', 'right', 'left')
    compare_modes = ('ratio', 'difference')
    
    def __init__(self, fold_mode: str = 'fold', compare_mode: str = 'ratio', control_index=0,
                 base_indices=None, comb_indices=None):
        self.fold_mode = fold_mode
        self.compare_mode = compare_mode
        self.control_index = control_index
        self.base_indices = base_indices
        self.comb_indices = comb_indices
    
    @staticmethod
    def create_process(cluster_block):
        return Process(cluster_block)


class Process(base.ElementProcess):
    def __init__(self, cluster_block):
        super().__init__(process_func, Conf(), cluster_block)


def process_func(sp_result_list, conf: Conf):
    sp_list = tuple(np.array(sp) for sp, _ in sp_result_list)
    x, yv_list, center_i = align_list(sp_list, conf.control_index)
    x, yv_list = fold_list(x, yv_list, center_i, conf.fold_mode)
    yv_list = tuple(divide_var(y, y_var, *sum_var(y, y_var)) for y, y_var in yv_list)
    yv_list = compare_list(yv_list, conf.compare_mode, conf.control_index)
    curve_list = tuple((x, y, y_var) for y, y_var in yv_list)
    component_result = None if conf.base_indices is None \
        else process_components(yv_list, conf.base_indices, conf.comb_indices, conf.control_index)
    return curve_list, component_result


# utils

def align_list(sp_list, control_index=None):
    # todo recode if the x is not the same
    control_index = 0 if control_index is None else control_index
    
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
    if mode == 'fold':
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
    elif mode == 'none':
        return x, yv_list
    elif mode == 'right':
        x_right = x[center_i:] - x[center_i]
        yv_right_list = yv_list[:, :, center_i:]
        return x_right, yv_right_list
    elif mode == 'left':
        x_left = x[center_i] - x[:center_i + 1]
        yv_left_list = yv_list[:, :, :center_i + 1]
        return np.flip(x_left), np.flip(yv_left_list, 2)
    else:
        raise TypeError("Unsupported fold mode")


def compare_list(yv_list, mode, control_index=None):
    control_yv = None if control_index is None else yv_list[control_index]
    return list(compare_yv(yv, control_yv, mode, i == control_index) for i, yv in enumerate(yv_list))


def compare_yv(yv, control_yv, mode, is_control=False):
    """
    :return: c, c_var
    """
    y, y_var = yv
    if mode == 'ratio':
        if is_control:
            return np.ones_like(y), np.zeros_like(y_var)
        control_y, control_y_var = (1, 0) if control_yv is None else control_yv
        return divide_var(y, y_var, control_y, control_y_var)
    elif mode == 'difference':
        if is_control:
            return np.zeros_like(y), np.zeros_like(y_var)
        control_y, control_y_var = (0, 0) if control_yv is None else control_yv
        return minus_var(y, y_var, control_y, control_y_var)
    else:
        raise TypeError(f"Unsupported compare mode {mode}")


def process_components(yv_list, base_indices, comb_indices, control_index):
    y_list = tuple(y for y, _ in yv_list)
    if control_index in base_indices:
        raise TypeError("base_indices should not contains control_index!")
    if comb_indices is None:
        comb_indices = tuple(filter(lambda i: i != control_index and i not in base_indices, range(len(y_list))))
    elif control_index in comb_indices:
        raise TypeError("comb_indices should not contains control_index!")
    
    base_list = np.take(y_list, base_indices, 0)  # [nb,n]
    comb_list = np.take(y_list, comb_indices, 0)  # [nc,n]
    return tuple(fit_y2(y, base_list) for y in comb_list)


def fit_y(y, base_list):
    # y [n]
    # base_list [nb,n]
    func = lambda theta: np.sum(base_list * np.expand_dims(theta, -1), 0)
    loss = lambda theta: np.sum(np.square(func(theta) - y))
    
    theta0 = np.zeros([len(base_list)])  # theta [nb]
    res: opt.OptimizeResult = opt.minimize(loss, theta0)
    
    if not res.success:
        return None
    
    theta_opt = res.x
    sigma_opt = np.sqrt(np.mean(np.square(func(theta_opt) - y)))
    return theta_opt, sigma_opt


def fit_y2(y, base_list):
    # y [n]
    # base_list [nb,n]
    p = np.sum(np.expand_dims(base_list, 0) * np.expand_dims(base_list, 1), -1)  # [nb,nb]
    b = np.sum(np.expand_dims(y, 0) * base_list, -1, keepdims=True)  # [nb,1]
    theta = np.dot(np.linalg.inv(p), b)
    sigma = np.sqrt(np.mean(np.square(np.sum(base_list * np.expand_dims(theta, -1), 0) - y)))
    return theta, sigma
