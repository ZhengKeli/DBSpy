import abc


class BaseProcess(abc.ABC):
    
    def __init__(self):
        self.result = None
    
    def process(self, *args, **kwargs):
        self.result = None
        self.result = self.on_process(*args, **kwargs)
        return self.result
    
    def try_process(self, *args, **kwargs):
        try:
            return self.process(*args, **kwargs)
        except Exception:
            return None
    
    @abc.abstractmethod
    def on_process(self, *args, **kwargs):
        pass
