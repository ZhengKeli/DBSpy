import abc

from spector.core.base import BaseProcess


class BaseConf(abc.ABC):
    
    @abc.abstractmethod
    def apply(self, process: BaseProcess):
        pass
    
    @staticmethod
    @abc.abstractmethod
    def reset(process: BaseProcess):
        pass
    
    @abc.abstractmethod
    def encode(self):
        pass
    
    @staticmethod
    @abc.abstractmethod
    def decode(code):
        pass
