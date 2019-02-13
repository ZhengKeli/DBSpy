import abc


class ProcessBlock:
    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        self.result = None
    
    def process(self, *args, **kwargs):
        self.result = self.on_process(*args, **kwargs)
        return self.result
    
    @abc.abstractmethod
    def on_process(self, *args, **kwargs):
        pass
