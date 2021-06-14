from colorama import Fore
from abc import ABC, abstractmethod
import os
from os.path import join, isdir, isfile, dirname
from base64 import b64encode
from functools import lru_cache
from io import BytesIO
import config
from datetime import datetime
from .path import touch
import logging

LOGGING_PATH = join(config.SRC_PATH, config.get('logging/path'))
assert isdir(LOGGING_PATH)


def get_logging_file() -> str:
    def _get_dir(year: str, month: str) -> str:
        _path = join(LOGGING_PATH, year, month)
        if not isdir(_path):
            os.makedirs(_path)
        return _path
    t = datetime.today()
    filename = t.strftime('%Y-%m-%d.log')
    path = join(_get_dir(str(t.year), t.strftime("%B")), filename)
    if not isfile(path):
        touch(path)
    return path


class Logger(ABC):
    @abstractmethod
    def info(self, msg):
        pass

    @abstractmethod
    def debug(self, msg):
        pass

    @abstractmethod
    def warning(self, msg):
        pass

    @abstractmethod
    def error(self, msg):
        pass


class DefaultLogger(Logger):
    def __init__(self, name: str, level: int = logging.DEBUG):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logging_file = get_logging_file()
        handler = logging.FileHandler(self.logging_file, 'a', 'utf-8')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def info(self, s: str):
        self.logger.info(s)

    def debug(self, s: str):
        self.logger.debug(s)

    def warning(self, s: str):
        self.logger.warning(s)

    def error(self, s: str):
        self.logger.error(s)


class ConsoleLogger(Logger):
    def __init__(self, name: str):
        self.format = '{asctime} - {name} - {levelname} - {message}'
        self.name = name

    def _get_formatted_msg(self, msg, level):
        t = datetime.today()
        res = self.format.format(asctime=t.strftime('%Y-%m-%d-%H:%M:%S'),
                                 name=self.name,
                                 levelname=level,
                                 message=msg)
        return res

    def info(self, s: str):
        msg = self._get_formatted_msg(s, 'INFO')
        print('{}{}{} '.format(Fore.GREEN, msg, Fore.RESET))

    def debug(self, s: str):
        msg = self._get_formatted_msg(s, 'DEBUG')
        print('{}{}{} '.format(Fore.MAGENTA, msg, Fore.RESET))

    def warning(self, s):
        msg = self._get_formatted_msg(s, 'WARNING')
        print('{}{}{} '.format(Fore.YELLOW, msg, Fore.RESET))

    def error(self, s: str):
        msg = self._get_formatted_msg(s, 'ERROR')
        print('{}{}{} '.format(Fore.RED, msg, Fore.RESET))


class CmdLogger(Logger):
    def __init__(self, name):
        self.name = name

    def info(self, s: str):
        print('({})'.format(self.name), end='')
        print('{}[INFO]{} '.format(Fore.GREEN, Fore.RESET), end='')
        print(s)

    def debug(self, s: str):
        print('({})'.format(self.name), end='')
        print('{}[DEBUG]{} '.format(Fore.MAGENTA, Fore.RESET), end='')
        print(s)

    def warning(self, s):
        print('({})'.format(self.name), end='')
        print('{}[WARNING]{} '.format(Fore.YELLOW, Fore.RESET), end='')
        print(s)

    def error(self, s: str):
        print('({})'.format(self.name), end='')
        print('{}[ERROR]{} '.format(Fore.RED, Fore.RESET), end='')
        print(s)


class RichLogger:
    def __init__(self, filename: str, overwrite=False):
        self.f = None
        self.filename = filename
        self.overwrite = overwrite

    def ensure_file(self):
        if self.f is not None:
            return
        self.f = open(self.filename, 'wb' if self.overwrite else 'ab')
        if self.f.tell() == 0:
            self.loghtml('<html><head><meta charset="utf-8"></head><body>')

    def logimage(self, image):
        self.ensure_file()
        bio = BytesIO()
        image.save(bio, format='PNG')
        imgb64 = b64encode(bio.getvalue())
        self.f.write(b'<p><img src="data:image/png;base64,%s" /></p>\n' % imgb64)
        self.f.flush()

    def logtext(self, text):
        self.ensure_file()
        self.loghtml('<pre>%s</pre>\n' % text)

    def loghtml(self, html):
        self.ensure_file()
        self.f.write(html.encode())
        self.f.flush()


@lru_cache(maxsize=None)
def get_logger(module):
    import config
    if config.get_instance_id() == 0:
        filename = '%s.html' % module
    else:
        filename = '%s.%d.html' % (module, config.get_instance_id())
    logger = RichLogger(os.path.join(config.logs, filename), True)
    return logger

# @lru_cache(maxsize=None)
# def get_logger(module):
#     # import config
#     # if config.get_instance_id() == 0:
#     #     filename = '%s.html' % module
#     # else:
#     #     filename = '%s.%d.html' % (module, config.get_instance_id())
#     # logger = RichLogger(os.path.join(config.logs, filename), True)
#
#     return logger
