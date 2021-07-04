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
from abc import ABC, abstractmethod
from . import HidingLock
from colorama import Fore

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
    def _get_dir(year: str, month: str) -> str:
        _path = join(LOGGING_PATH, year, month)
        if not isdir(_path):
            os.makedirs(_path)
        return _path
    t = datetime.today()
    filename = t.strftime('%Y-%m-%d.log.html')
    path = join(_get_dir(str(t.year), t.strftime("%B")), filename)
    if not isfile(path):
        copyfile(join(_resource_path, 'log_temp.html'),
                 path)
    return path


logging_file_path = get_logging_file()
with open(logging_file_path) as f:
    logging_soup = HidingLock(BeautifulSoup(f, features="html.parser"))


def _pil2b64(img: Image):
    bio = BytesIO()
    img.save(bio, format='PNG')
    img_b64 = b64encode(bio.getvalue())
    return img_b64


def _save_on_exist():
    with logging_soup as soup:
        with open(logging_file_path) as _f:
            _f.write(str(soup))


class HTMLLogger(ABC):
    @abstractmethod
    def info(self, msg, image):
        pass

    @abstractmethod
    def debug(self, msg, image):
        pass

    @abstractmethod
    def warning(self, msg, image):
        pass

    @abstractmethod
    def error(self, msg, image):
        pass


class VisualLogger(HTMLLogger):
    def __init__(self, name, sub_logger=None):
        self.name = name
        self.format = '{asctime} - {name} - {levelname} - {message}'
        # load templates
        with open(join(_resource_path, 'img_entry.html')) as _f:
            self.img_entry_temp = BeautifulSoup(_f, features="html.parser").find('a')
        with open(join(_resource_path, 'text_entry.html')) as _f:
            self.text_entry_temp = BeautifulSoup(_f, features="html.parser").find('a')
        # sub logger
        self.sub_logger = sub_logger
        pass

    # def _load_log(self):
    #     with open(self.logging_file) as _f:
    #         self.log_soup = BeautifulSoup(_f, features="html.parser")
    #
    # def _save_log(self):
    #     with open(self.logging_file, "w") as _f:
    #         _f.write(str(self.log_soup))
    def __del__(self):
        self.debug('logger [{}] is closed'.format(self.name))
        _save_on_exist()

    @staticmethod
    def _get_entry_num():
        with logging_soup as soup:
            list_ = soup.findAll('a', class_="list-group-item")
        return len(list_)

    def _write_entry(self, msg: str, image: list or Image, msg_color: str = None):
        assert not (msg is None and image is None)
        if not isinstance(image, list) and image is not None:
            image = [image]
        # make entry
        if image is None:
            text_entry = copy(self.text_entry_temp)
            text_entry.string = msg
            entry = text_entry
        else:
            num = self._get_entry_num()
            img_entry = copy(self.img_entry_temp)
            img_entry.span.insert_before(msg)
            img_entry['data-target'] = '#{}'.format(num)
            img_entry.span.string = '{}'.format(len(image))
            img_entry.div['id'] = '{}'.format(num)
            for img in image:
                img_tag = img_entry.new_tag('p')
                img_tag.append(
                    img_entry.new_tag("img",
                                      src='data:image/png;base64,%s' % _pil2b64(img).decode("utf-8"))
                )
                img_entry.div.append(img_tag)
            entry = img_entry
        if msg_color is not None:
            entry['style'] = 'color:{};'.format(msg_color)
        # add to soup
        with logging_soup as soup:
            soup.html.body.div.append(entry)

    def _get_formatted_msg(self, msg, level):
        t = datetime.today()
        res = self.format.format(asctime=t.strftime('%Y-%m-%d-%H:%M:%S'),
                                 name=self.name,
                                 levelname=level,
                                 message=msg)
        return res

    def info(self, msg: str = None, image: list or Image = None):
        formatted_msg = self._get_formatted_msg(msg, 'INFO')
        self._write_entry(formatted_msg, image, COLOR_PICKER['INFO'])
        if self.sub_logger is not None:
            self.sub_logger.info(msg)

    def debug(self, msg: str = None, image: list or Image = None):
        formatted_msg = self._get_formatted_msg(msg, 'DEBUG')
        self._write_entry(formatted_msg, image, COLOR_PICKER['DEBUG'])
        if self.sub_logger is not None:
            self.sub_logger.debug(msg)

    def warning(self, msg: str = None, image: list or Image = None):
        formatted_msg = self._get_formatted_msg(msg, 'WARNING')
        self._write_entry(formatted_msg, image, COLOR_PICKER['WARNING'])
        if self.sub_logger is not None:
            self.sub_logger.warning(msg)

    def error(self, msg: str = None, image: list or Image = None):
        formatted_msg = self._get_formatted_msg(msg, 'ERROR')
        self._write_entry(formatted_msg, image, COLOR_PICKER['ERROR'])
        if self.sub_logger is not None:
            self.sub_logger.error(msg)


class DummyLogger(HTMLLogger):
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

    def info(self, msg, image=None):
        msg = self._get_formatted_msg(msg, 'INFO')
        print('{}{}{} '.format(Fore.GREEN, msg, Fore.RESET))

    def debug(self, msg, image=None):
        msg = self._get_formatted_msg(msg, 'DEBUG')
        print('{}{}{} '.format(Fore.MAGENTA, msg, Fore.RESET))

    def warning(self, msg, image=None):
        msg = self._get_formatted_msg(msg, 'WARNING')
        print('{}{}{} '.format(Fore.YELLOW, msg, Fore.RESET))

    def error(self, msg, image=None):
        msg = self._get_formatted_msg(msg, 'ERROR')
        print('{}{}{} '.format(Fore.RED, msg, Fore.RESET))


if __name__ == '__main__':
    logger = VisualLogger('hhh')
