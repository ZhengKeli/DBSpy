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


@DeprecationWarning
class IndexedValue:
    def __init__(self, index: int, value):
        self.index = index
        self.value = value
    
    @staticmethod
    def by_index(xs, index):
        return IndexedValue(index, xs[index])
    
    @staticmethod
    def by_value(xs, value):
        return IndexedValue(index_nearest(value, xs), value)


@DeprecationWarning
class IndexedRange:
    def __init__(self, head: IndexedValue, tail: IndexedValue):
        self.head = head
        self.tail = tail
    
    @staticmethod
    def by_index(xs, head_index, tail_index):
        return IndexedRange(IndexedValue.by_index(xs, head_index), IndexedValue.by_index(xs, tail_index))
    
    @staticmethod
    def by_value(xs, head_value, tail_value):
        return IndexedRange(IndexedValue.by_value(xs, head_value), IndexedValue.by_value(xs, tail_value))
    
    @property
    def to_slice(self):
        return slice(self.head.index, self.tail.index)
