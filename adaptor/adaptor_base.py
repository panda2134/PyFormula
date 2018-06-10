from abc import *
from PyQt5.QtGui import QImage


class AdaptorBase(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def parseLaTeX(formula) -> QImage:
        pass
