import abc

from dbspy.core import base


class Conf(base.Conf, abc.ABC):
    
    @staticmethod
    @abc.abstractmethod
    def create_process():
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
            **self.encode_content()
        }
    
    @classmethod
    def decode(cls, code):
        from . import dbs, cdbs
        c = {'dbspy': dbs.Conf, 'cdbs': cdbs.Conf}[code['type']]
        content_code = code.copy()
        del content_code['type']
        return c.decode_content(content_code)
    
    @abc.abstractmethod
    def encode_content(self):
        pass
    
    @classmethod
    @abc.abstractmethod
    def decode_content(cls, code):
        pass
