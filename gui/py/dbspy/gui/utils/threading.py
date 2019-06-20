from threading import Lock


def synchronized(func):
    func.__lock__ = Lock()
    
    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)
    
    return synced_func
