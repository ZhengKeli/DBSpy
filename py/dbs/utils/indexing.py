from collections import Iterable


def search_nearest(x_head, x_tail, x_step, y, func):
    if isinstance(y, dict):
        return dict((k, search_nearest(x_head, x_tail, x_step, vk, func)) for (k, vk) in y.items())
    if isinstance(y, Iterable):
        return tuple(search_nearest(x_head, x_tail, x_step, yi, func) for yi in y)
    
    x_last = x_head
    y_last = func(x_last)
    asc = y_last < y
    x_this = x_last + x_step
    while x_this < x_tail:
        y_this = func(x_this)
        if (y_this < y) != asc:
            if (y_this - y < y - y_last) == asc:
                return x_this, y_this
            else:
                return x_last, y_last
        x_last = x_this
        y_last = y_this
        x_this += x_step
    return x_last, y_last


def index_nearest(value, array):
    if isinstance(value, dict):
        return dict((k, index_nearest(vk, array)) for (k, vk) in value.items())
    if isinstance(value, Iterable):
        return tuple(index_nearest(vi, array) for vi in value)
    return search_nearest(0, len(array), 1, value, lambda i: array[i])[0]
