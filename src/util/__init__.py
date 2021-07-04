import functools
import threading


# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


# https://stackoverflow.com/questions/38978652/how-to-protect-an-object-using-a-lock-in-python
class HidingLock(object):
    def __init__(self, obj, lock=None):
        self.lock = lock or threading.RLock()
        self._obj = obj

    def __enter__(self):
        self.lock.acquire()
        return self._obj

    def __exit__(self, exc_type, exc_value, traceback):
        self.lock.release()

    def set(self, obj):
        with self:
            self._obj = obj


def synchronized(wrapped=None, lock=None):
    if wrapped is None:
        return functools.partial(synchronized, lock=lock)
    if lock is None:
        lock = threading.RLock()

    @functools.wraps(wrapped)
    def _wrapper(*args, **kwargs):
        with lock:
            return wrapped(*args, **kwargs)

    return _wrapper
