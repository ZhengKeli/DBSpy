class Block:
    def __init__(self, value=None):
        self._version = 0
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        self._version += 1
    
    @property
    def version(self):
        return self._version
    
    @property
    def release(self):
        return self._value, self._version


class FunctionBlock(Block):
    def __init__(self, func, *arg_blocks):
        self._func = func
        self._arg_blocks = list(arg_blocks)
        self._buffer_versions = None
        super().__init__()
    
    def invalidate(self):
        self._buffer_versions = None
    
    @property
    def func(self):
        return self._func
    
    @property
    def arg_blocks(self):
        return tuple(self._arg_blocks)
    
    def check(self):
        latest_arg_values, latest_arg_versions = zip(*(block.release for block in self.arg_blocks))
        valid = (self._buffer_versions is not None) and all(
            b == l for b, l in zip(self._buffer_versions, latest_arg_versions))
        if not valid:
            self._buffer_versions = latest_arg_versions
            self.value = self.func(*latest_arg_values)
    
    @Block.value.getter
    def value(self):
        self.check()
        return super().value
    
    @property
    def version(self):
        self.check()
        return super().version
    
    @property
    def release(self):
        self.check()
        return super().release


class ClusterBlock(FunctionBlock):
    def __init__(self, *blocks):
        super().__init__(lambda *args: args, blocks)
    
    @property
    def blocks(self):
        return self._arg_blocks
    
    @blocks.setter
    def blocks(self, blocks):
        self._arg_blocks = blocks
        self.invalidate()
