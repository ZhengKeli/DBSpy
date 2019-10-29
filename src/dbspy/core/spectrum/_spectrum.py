import abc

from dbspy.core import base


class Conf(base.Conf, abc.ABC):
    
    def __init__(self, tag=None):
        self.tag = tag
    
    @abc.abstractmethod
    def create_process(self):
        pass
    
    def create_and_apply(self):
        process = self.create_process()
        self.apply(process)
        return process
    
    def encode(self):
        from . import dbs, cdbs
        t = {dbs.Conf: 'dbspy', cdbs.Conf: 'cdbs'}[type(self)]
        return {
            'type': t,
            'tag': self.tag,
            **self.encode_content()
        }
    
    @classmethod
    def decode(cls, code):
        from . import dbs, cdbs
        c = {'dbspy': dbs.Conf, 'cdbs': cdbs.Conf}[code['type']]
        tag = code['tag']
        content_code = code.copy()
        del content_code['type']
        del content_code['tag']
        return c.decode_content(tag, content_code)
    
    @abc.abstractmethod
    def encode_content(self):
        pass
    
    @classmethod
    @abc.abstractmethod
    def decode_content(cls, tag, code):
        pass


class Process(base.Process, abc.ABC):
    
    def __init__(self, block, tag):
        super().__init__(block)
        self.tag = tag
