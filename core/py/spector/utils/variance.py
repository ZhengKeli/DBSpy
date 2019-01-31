import numpy as np


def compute_sp_var(ys, ys_sum=None):
    if ys_sum is None:
        ys_sum = np.sum(ys)
    return ys * (1 - ys / ys_sum)


def compute_add_var(x1, x1_var, x2, x2_var):
    y = x1 + x2
    y_var = x1_var + x2_var
    return y, y_var


def compute_minus_var(x1, x1_var, x2, x2_var):
    y = x1 - x2
    y_var = x1_var + x2_var
    return y, y_var


def compute_times_var(x1, x1_var, x2, x2_var):
    y = x1 * x2
    y_var = np.square(y) * (x1_var / np.square(x1) + x2_var / np.square(x2))
    return y, y_var


def compute_divide_var(x1, x1_var, x2, x2_var):
    y = x1 / x2
    y_var = np.square(y) * (x1_var / np.square(x1) + x2_var / np.square(x2))
    return y, y_var
