import abc


class BaseProcess:
    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        self.result = None
    
    def process(self, *args, **kwargs):
        try:
            self.result = self.on_process(*args, **kwargs)
            return self.result
        except Exception as exception:
            self.result = None
            raise exception

    def try_process(self, *args, **kwargs):
        try:
            return self.process(*args, **kwargs)
        except Exception:
            return None
    
    @abc.abstractmethod
    def on_process(self, *args, **kwargs):
        pass
