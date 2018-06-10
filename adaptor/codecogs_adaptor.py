from PyQt5.QtGui import QImage
from adaptor.adaptor_base import AdaptorBase
from urllib.request import urlopen
from urllib.parse import quote

codecogs = 'http://latex.codecogs.com/gif.latex?'


class CodeCogsAdaptor(AdaptorBase):
    @staticmethod
    def parseLaTeX(formula) -> QImage:
        img_raw = urlopen(codecogs + quote(formula)).read()
        img = QImage()
        img.loadFromData(img_raw)
        return img
