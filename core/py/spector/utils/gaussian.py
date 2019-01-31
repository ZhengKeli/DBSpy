import numpy as np
from scipy import optimize


def gaussian_func(x, args):
    a, b, c, d = args
    return a * np.exp(-(x - b) ** 2 / (2 * c ** 2)) + d


def gaussian_fit_init_args(points):
    xs, ys = np.array(points).transpose()
    dx = xs[1] - xs[0]
    peak_index = np.argmax(ys)
    a = ys[peak_index]
    b = xs[peak_index]
    d = np.min(ys)
    c = dx * np.sum(ys - d) / np.sqrt(2.0 * np.pi) / a
    return np.array((a, b, c, d), np.float)


def gaussian_fit(points):
    init_args = gaussian_fit_init_args(points)
    result = optimize.leastsq(
        lambda args, xs, ys: gaussian_func(xs, args) - ys,
        init_args, (points[:, 0], points[:, 1]))
    return result[0]


def gaussian_fwhm(args):
    return 2 * args[2] * np.sqrt(2 * np.log(2))
