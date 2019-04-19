def search_nearest(x_head, x_tail, x_step, y, func):
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
    return search_nearest(0, len(array), 1, value, lambda i: array[i])[0]
