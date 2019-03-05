def search_nearest(x_head, x_tail, x_step, y, func):
    x_last = x_head
    y_last = func(x_last)
    asc = y_last < y
    x = x_last + x_step
    while x < x_tail:
        yx = func(x)
        if (yx < y) != asc:
            if (yx - y < y - y_last) == asc:
                return x, y
            else:
                return x_last, y_last
        x_last = x
        y_last = y
        x = x_last + x_step
    return x_last, y_last


def index_nearest(x, xs):
    return search_nearest(0, len(xs), 1, x, lambda i: xs[i])[0]
