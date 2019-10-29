import numpy as np


def add_var(x1, x1_var, x2, x2_var):
    y = x1 + x2
    y_var = x1_var + x2_var
    return y, y_var


def minus_var(x1, x1_var, x2, x2_var):
    y = x1 - x2
    y_var = x1_var + x2_var
    return y, y_var


def times_var(x1, x1_var, x2, x2_var):
    y = x1 * x2
    y_var = np.square(x2) * x1_var + np.square(x1) * x2_var
    return y, y_var


def divide_var(x1, x1_var, x2, x2_var):
    y = x1 / x2
    y_var = x1_var / np.square(x2) + np.square(x1 / x2 / x2) * x2_var
    return y, y_var


def sum_var(x, x_var, axis=None):
    return np.sum(x, axis), np.sum(x_var, axis)


def mean_var(x, x_var, axis=None):
    return divide_var(*sum_var(x, x_var, axis), len(x), 0)


def spectrum_var(ys, ys_sum=None):
    if ys_sum is None:
        ys_sum = np.sum(ys)
    return ys * (1 - ys / ys_sum) + 1 / 3
