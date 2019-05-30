import abc
import tkinter as tk

from dbspy.core.base import Process, ElementConf, ElementProcess


class ProcessController(abc.ABC):
    def __init__(self, container: tk.Frame, process: Process):
        self.process = process
        self.create_root_frame(container)
        self.init()
    
    def create_root_frame(self, container):
        root_frame = tk.Frame(container)
        root_frame.pack(fill='both')
        self.on_create_root_frame(root_frame)
    
    def on_create_root_frame(self, root_frame):
        self.create_info_frame(root_frame)
        self.create_result_frame(root_frame)
    
    def create_info_frame(self, root_frame):
        info_frame = tk.Frame(root_frame)
        info_frame.pack(fill='x')
        self.on_create_info_frame(info_frame)
    
    @abc.abstractmethod
    def on_create_info_frame(self, info_frame):
        pass
    
    def create_result_frame(self, root_frame):
        result_frame = tk.LabelFrame(root_frame, text='Result:')
        result_frame.pack(fill='both')
        self.on_create_result_frame(result_frame)
    
    @abc.abstractmethod
    def on_create_result_frame(self, result_frame):
        pass
    
    def init(self):
        self.update()
    
    def update(self):
        try:
            self.on_update(self.process.value, None)
        except Exception as exception:
            self.on_update(None, exception)
            raise
    
    @abc.abstractmethod
    def on_update(self, result, exception):
        pass


class ElementProcessController(ProcessController, abc.ABC):
    def __init__(self, container: tk.Frame, process: ElementProcess):
        super().__init__(container, process)
    
    def on_create_root_frame(self, root_frame):
        self.create_info_frame(root_frame)
        self.create_conf_frame(root_frame)
        self.create_operate_frame(root_frame)
        self.create_result_frame(root_frame)
    
    def create_conf_frame(self, root_frame):
        conf_frame = tk.LabelFrame(root_frame, text='Configurations')
        conf_frame.pack(fill='x')
        self.on_create_conf_frame(conf_frame)
    
    @abc.abstractmethod
    def on_create_conf_frame(self, conf_frame):
        pass
    
    def create_operate_frame(self, root_frame):
        operate_frame = tk.Frame(root_frame)
        operate_frame.pack(fill='x')
        tk.Button(operate_frame, text='Apply', command=self.apply).pack(side='left')
        tk.Button(operate_frame, text='Reset', command=self.reset).pack(side='left')
        self.on_create_operate_frame(operate_frame)
    
    def on_create_operate_frame(self, operate_frame):
        pass
    
    def init(self):
        self.reset()
        self.update()
    
    def reset(self):
        self.on_reset(self.process.conf)
        self.update()
    
    @abc.abstractmethod
    def on_reset(self, conf: ElementConf):
        pass
    
    def apply(self):
        self.process.conf = self.on_apply()
        self.update()
    
    @abc.abstractmethod
    def on_apply(self) -> ElementConf:
        pass
