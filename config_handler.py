import os
from configparser import *

from adaptor.codecogs_adaptor import CodeCogsAdaptor
from adaptor.zhihu_adaptor import ZhihuAdaptor

defaults = {
    'AlwaysTop': True,
    'ListenToClip': True,
    'Render': 'Zhihu',
    'WaitTime': 1000
}

cfg = ConfigParser(defaults)


def write_to_file():
    cfg.write(open('pyformula.ini', 'w'))


def read_from_file():
    if not os.path.exists('pyformula.ini'):
        write_to_file()
    cfg.read_file(open('pyformula.ini', 'r'))


def get_formula_adaptor():
    if cfg.get('DEFAULT', 'Render') == 'CodeCogs':
        return CodeCogsAdaptor
    elif cfg.get('DEFAULT', 'Render') == 'Zhihu':
        return ZhihuAdaptor
    else:
        raise ValueError('Unsupported render engine')


def get_config_parser():
    return cfg






read_from_file()
