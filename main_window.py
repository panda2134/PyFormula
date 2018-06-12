from types import MethodType
from urllib.error import URLError

from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QMimeData
from PyQt5.QtGui import QPixmap, QImage, QDrag
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

import config_handler
from about_dialog import AboutDialog
from settings_dialog import SettingsDialog


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


def mouseMoveEvent(self, event):
    if event.buttons() != Qt.LeftButton:
        return

    mime = QMimeData()
    mime.setImageData(self.pixmap()) # buggy
    print(self.pixmap())

    drag = QDrag(self)
    drag.setMimeData(mime)

    drag.exec(Qt.MoveAction)


class MainWindow(QMainWindow):
    waiting = False
    down_thread = None
    img = None

    @staticmethod
    def show_about():
        AboutDialog().exec()

    @staticmethod
    def show_settings():
        SettingsDialog().exec()

    @staticmethod
    def scale_image_to_label(img, lbl):
        img_size = img.size()
        lbl_size = lbl.size()
        width_rto = img_size.width() / lbl_size.width()
        height_rto = img_size.height() / lbl_size.height()
        if width_rto > height_rto:
            return img.scaledToWidth(lbl_size.width(), Qt.SmoothTransformation)
        else:
            return img.scaledToHeight(lbl_size.height(), Qt.SmoothTransformation)

    def load_image_to_ui(self, img):
        if not (img is None):
            self.img = img
            img = MainWindow.scale_image_to_label(img, self.imgLabel)
            img = img.scaledToHeight(img.size().height() * .50, Qt.SmoothTransformation)
            pixmap = QPixmap.fromImage(img)
            self.imgLabel.setPixmap(pixmap)
            self.statusBar().showMessage('Connected.')
        else:
            self.img = None
            self.statusBar().showMessage('Disconnected.')
        self.waiting = False

    def update_impl(self):
        adp = config_handler.get_formula_adaptor()
        text = self.plainTextEdit.toPlainText()
        self.down_thread = ImageDownloadThread(adp, text)
        self.down_thread.finish_signal.connect(self.load_image_to_ui)
        self.down_thread.start()

    def update_image(self):
        if not self.waiting:
            self.waiting = True
            wait_time = int(config_handler.get_config_parser().get('DEFAULT', 'WaitTime'))
            QTimer().singleShot(wait_time, self.update_impl)

    def __init__(self):
        if config_handler.get_config_parser().getboolean('DEFAULT', 'AlwaysTop'):
            super().__init__(None, Qt.WindowStaysOnTopHint)
        else:
            super().__init__()

        loadUi('ui/main.ui', self)
        # self.imgLabel.setDragEnabled(True)
        self.imgLabel.mouseMoveEvent = MethodType(mouseMoveEvent, self.imgLabel)

