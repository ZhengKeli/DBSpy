import abc

from dbspy.core import base


class Conf(base.ElementConf, abc.ABC):
    
    @staticmethod
    @abc.abstractmethod
    def create_process(cluster_block):
        pass
    
    def create_and_apply(self, cluster_block):
        process = self.create_process(cluster_block)
        self.apply(process)
        return process
    
    def encode(self) -> dict:
        from . import sw, curve
        t = {sw.Conf: 'sw', curve.Conf: 'curve'}[type(self)]
        return {
            'type': t,
            **self.encode_content()
        }
    
    @classmethod
    def decode(cls, code):
        from . import sw, curve
        c = {'sw': sw.Conf, 'curve': curve.Conf}[code['type']]
        content_code = code.copy()
        del content_code['type']
        return c.decode_content(content_code)
    
    @abc.abstractmethod
    def encode_content(self):
        super().encode()
    
    @classmethod
    def decode_content(cls, code):
        return super().decode(code)
