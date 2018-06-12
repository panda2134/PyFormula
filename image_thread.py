from urllib.error import URLError

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage


class ImageDownloadThread(QThread):
    finish_signal = pyqtSignal(QImage)

    def __init__(self, adp, text, parent=None):
        super(ImageDownloadThread, self).__init__(parent)
        self.adp = adp
        self.text = text

    def run(self):
        try:
            img = self.adp.parseLaTeX(self.text)
        except URLError:
            img = None
        self.finish_signal.emit(img)
