import abc

from dbs.core import base


class Conf(base.Conf, abc.ABC):
    
    @staticmethod
    @abc.abstractmethod
    def create_process(cluster_block):
        pass
    
    def create_and_apply(self, cluster_block):
        process = self.create_process(cluster_block)
        self.apply(process)
        return process
    
    def encode(self) -> dict:
        from . import sw, ratio
        t = {sw.Conf: 'sw', ratio.Conf: 'ratio'}[type(self)]
        return {
            'type': t,
            **self.encode_content()
        }
    
    @classmethod
    def decode(cls, code):
        from . import sw, ratio
        c = {'sw': sw.Conf, 'ratio': ratio.Conf}[code['type']]
        content_code = code.copy()
        del content_code['type']
        return c.decode_content(content_code)
    
    def encode_content(self):
        return super().encode()
    
    @classmethod
    def decode_content(cls, code):
        return super().decode(code)
