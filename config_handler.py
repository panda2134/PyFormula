import os
from configparser import *

defaults = {
    'AlwaysTop': True,
    'ListenToClip': True,
    'Render': 'CodeCogs'
}

cfg = ConfigParser(defaults)


def write_to_file():
    cfg.write(open('pyformula.ini', 'w'))


def read_from_file():
    if not os.path.exists('pyformula.ini'):
        write_to_file()
    cfg.read_file(open('pyformula.ini', 'r'))


def get_config_parser():
    return cfg






read_from_file()
