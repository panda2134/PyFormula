from PyQt5.QtGui import QImage
from adaptor.adaptor_base import AdaptorBase
from urllib.request import urlopen
from urllib.parse import quote

zhihu = 'https://www.zhihu.com/equation?tex='


class ZhihuAdaptor(AdaptorBase):
    @staticmethod
    def parseLaTeX(formula) -> QImage:
        img_raw = urlopen(zhihu + quote(formula)).read()
        img = QImage()
        img.loadFromData(img_raw)
        return img
