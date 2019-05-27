import abc
from copy import deepcopy

from dbspy.utils.block import Block, FunctionBlock


class Process(abc.ABC):
    def __init__(self, block):
        self._block = block
    
    @property
    def block(self):
        return self._block
    
    @property
    def value(self):
        return self.block.value
    
    @property
    @abc.abstractmethod
    def conf(self):
        pass
    
    @conf.setter
    @abc.abstractmethod
    def conf(self, value):
        pass


class ElementProcess(Process, abc.ABC):
    def __init__(self, process_func, init_conf, *input_blocks):
        self.process_func = process_func
        self.conf_block = Block(init_conf)
        super().__init__(FunctionBlock(self.process_func, *input_blocks, self.conf_block))
    
    @property
    def conf(self):
        return deepcopy(self.conf_block.value)
    
    @conf.setter
    def conf(self, conf):
        self.conf_block.value = deepcopy(conf)


class Conf(abc.ABC):
    
    def apply(self, process: Process):
        process.conf = self
    
    @classmethod
    def reset(cls, process: Process):
        return process.conf
    
    @abc.abstractmethod
    def encode(self) -> dict:
        pass
    
    @classmethod
    @abc.abstractmethod
    def decode(cls, code: dict):
        pass


class ElementConf(Conf, abc.ABC):
    
    def keys(self):
        return (
            name for name in dir(self)
            if not name.startswith('_')
            if not callable(getattr(self, name)))
    
    def encode(self):
        return dict((key, getattr(self, key)) for key in self.keys())
    
    @classmethod
    def decode(cls, code):
        instance = cls()
        for key in instance.keys():
            setattr(instance, key, code[key])
        return instance
