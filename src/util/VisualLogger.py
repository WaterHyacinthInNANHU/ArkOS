from bs4 import BeautifulSoup
from os.path import dirname, realpath, join, isdir, isfile
from shutil import copyfile
import os
from base64 import b64encode
from io import BytesIO
from datetime import datetime
from copy import copy
from PIL import Image
import config
from colorama import Fore
from time import time_ns
from threading import RLock
from . import run_once
import atexit


def pil2b64(img: Image):
    bio = BytesIO()
    img.save(bio, format='PNG')
    img_b64 = b64encode(bio.getvalue())
    return img_b64


# resource path
_dir_path = dirname(realpath(__file__))
_resource_path = join(_dir_path, 'resources')

# logging path
LOGGING_PATH = join(config.SRC_PATH, config.get('logging/path'))
assert isdir(LOGGING_PATH)

# color picker
COLOR_PICKER = {'INFO': '#2ECC71', 'DEBUG': '#9B59B6', 'WARNING': '#F39C12', 'ERROR': '#E74C3C'}


# init logging file and soup
def get_logging_file() -> str:
    """
    get path of logging file
    :return: path in string
    """

    def _get_dir(year: str, month: str, day: str) -> str:
        _path = join(LOGGING_PATH, year, month, day)
        if not isdir(_path):
            os.makedirs(_path)
        return _path

    t = datetime.today()
    filename = t.strftime('%Y-%m-%d %H-%M-%S.%f.log.html')
    path = join(_get_dir(str(t.year), t.strftime("%B"), str(t.day)), filename)
    if not isfile(path):
        copyfile(join(_resource_path, 'log_temp_prefix.html'),
                 path)
    else:
        raise RuntimeError('log file already exists???')
    return path


LOGGING_FILE_PATH = get_logging_file()
LOGGING_FILE = open(LOGGING_FILE_PATH, 'a')


def _log(content: str):
    LOGGING_FILE.write(content)
    LOGGING_FILE.flush()


# load templates
with open(join(_resource_path, 'img_entry.html')) as _f:
    IMG_ENTRY_TEMP = BeautifulSoup(_f, features="html.parser")
with open(join(_resource_path, 'text_entry.html')) as _f:
    TEXT_ENTRY_TEMP = BeautifulSoup(_f, features="html.parser")


# write entry to log
def _write_entry(msg: str, image: list or Image, msg_color: str = None):
    def _get_id():
        return time_ns()

    assert not (msg is None and image is None)
    if not isinstance(image, list) and image is not None:
        image = [image]
    # make entry
    if image is None:
        text_entry = copy(TEXT_ENTRY_TEMP)
        text_entry.a.string = msg
        entry = text_entry
    else:
        id_ = _get_id()
        img_entry = copy(IMG_ENTRY_TEMP)
        img_entry.span.insert_before(msg)
        img_entry.a['data-target'] = '#{}'.format(id_)
        img_entry.span.string = '{}'.format(len(image))
        img_entry.div['id'] = '{}'.format(id_)
        for img in image:
            img_tag = img_entry.new_tag('p')
            img_tag.append(
                img_entry.new_tag("img",
                                  src='data:image/png;base64,%s' % pil2b64(img).decode("utf-8"))
            )
            img_entry.div.append(img_tag)
        entry = img_entry
    if msg_color is not None:
        entry['style'] = 'color:{};'.format(msg_color)
    # add to soup
    _log(str(entry) + '\n')


_write_lock = RLock()


def write_entry(msg: str, image: list or Image, msg_color: str = None):
    with _write_lock:
        _write_entry(msg, image, msg_color)


# add suffix after entries on exit
@run_once
def save():
    with open(join(_resource_path, 'log_temp_suffix.html')) as f:
        suffix = f.read()
    _log(suffix)


atexit.register(save)


class VisualLogger:
    def __init__(self, name, sub_logger=None):
        self.name = name
        self.format = '{asctime} - {name} - {levelname} - {message}'
        # sub logger
        self.sub_logger = sub_logger
        pass

    def _get_formatted_msg(self, msg, level):
        t = datetime.today()
        res = self.format.format(asctime=t.strftime('%Y-%m-%d-%H:%M:%S'),
                                 name=self.name,
                                 levelname=level,
                                 message=msg)
        return res

    def info(self, msg: str = None, image: list or Image = None):
        formatted_msg = self._get_formatted_msg(msg, 'INFO')
        write_entry(formatted_msg, image, COLOR_PICKER['INFO'])
        if self.sub_logger is not None:
            self.sub_logger.info(msg)

    def debug(self, msg: str = None, image: list or Image = None):
        formatted_msg = self._get_formatted_msg(msg, 'DEBUG')
        write_entry(formatted_msg, image, COLOR_PICKER['DEBUG'])
        if self.sub_logger is not None:
            self.sub_logger.debug(msg)

    def warning(self, msg: str = None, image: list or Image = None):
        formatted_msg = self._get_formatted_msg(msg, 'WARNING')
        write_entry(formatted_msg, image, COLOR_PICKER['WARNING'])
        if self.sub_logger is not None:
            self.sub_logger.warning(msg)

    def error(self, msg: str = None, image: list or Image = None):
        formatted_msg = self._get_formatted_msg(msg, 'ERROR')
        write_entry(formatted_msg, image, COLOR_PICKER['ERROR'])
        if self.sub_logger is not None:
            self.sub_logger.error(msg)

    @staticmethod
    def save():
        save()


class DummyLogger:
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

    def info(self, msg, _=None):
        msg = self._get_formatted_msg(msg, 'INFO')
        print('{}{}{} '.format(Fore.GREEN, msg, Fore.RESET))

    def debug(self, msg, _=None):
        msg = self._get_formatted_msg(msg, 'DEBUG')
        print('{}{}{} '.format(Fore.MAGENTA, msg, Fore.RESET))

    def warning(self, msg, _=None):
        msg = self._get_formatted_msg(msg, 'WARNING')
        print('{}{}{} '.format(Fore.YELLOW, msg, Fore.RESET))

    def error(self, msg, _=None):
        msg = self._get_formatted_msg(msg, 'ERROR')
        print('{}{}{} '.format(Fore.RED, msg, Fore.RESET))

    @staticmethod
    def save():
        pass
