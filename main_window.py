from types import MethodType

from PyQt5.QtCore import Qt, QTimer, QMimeData
from PyQt5.QtGui import QPixmap, QDrag, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

import config_handler
from about_dialog import AboutDialog
from image_thread import ImageDownloadThread
from settings_dialog import SettingsDialog
from utils import to_transparent_image


def mouseMoveEvent(self, event):
    if event.buttons() != Qt.LeftButton or self.window().img is None:
        return

    img_transparent = to_transparent_image(self.window().img)

    mime = QMimeData()
    mime.setImageData(img_transparent)

    drag = QDrag(self)
    drag.setMimeData(mime)
    drag.setPixmap(self.pixmap())

    drag.exec(Qt.MoveAction)


class MainWindow(QMainWindow):
    waiting = False
    down_thread = None
    img = None

    def init_window_flags(self, allow_top=True):
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint \
                            | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        if allow_top and config_handler.get_config_parser().getboolean('DEFAULT', 'AlwaysTop'):
            self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def show_about(self):
        self.init_window_flags(allow_top=False)
        AboutDialog().exec()
        self.init_window_flags(allow_top=True)
        self.show()

    def show_settings(self):
        config_handler.get_config_parser().getboolean('DEFAULT', 'AlwaysTop')
        self.init_window_flags(allow_top=False)
        SettingsDialog().exec()
        self.init_window_flags(allow_top=True)
        self.show()

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

    def load_image(self, img: QImage):
        if not (img is None):
            img = MainWindow.scale_image_to_label(img, self.imgLabel)
            img = img.scaledToHeight(img.size().height() * .50, Qt.SmoothTransformation)
            self.img = img
            pixmap = QPixmap.fromImage(img)
            self.imgLabel.setPixmap(pixmap)
            self.statusBar().showMessage('Connected.')
        else:
            self.img = None
            self.statusBar().showMessage('Disconnected.')

        if config_handler.get_config_parser().getboolean('DEFAULT', 'ListenToClip'):
            img_transparent = to_transparent_image(img)

            mime = QMimeData()
            mime.setImageData(img_transparent)

            QApplication.clipboard().setMimeData(mime)

        self.waiting = False

    def update_impl(self):
        adp = config_handler.get_formula_adaptor()
        text = self.plainTextEdit.toPlainText()
        self.down_thread = ImageDownloadThread(adp, text)
        self.down_thread.finish_signal.connect(self.load_image)
        self.down_thread.start()

    def update_image(self):
        if not self.waiting:
            self.waiting = True
            wait_time = int(config_handler.get_config_parser().get('DEFAULT', 'WaitTime'))
            QTimer().singleShot(wait_time, self.update_impl)

    def load_from_clipboard(self):
        text = QApplication.clipboard().text()
        sep = config_handler.get_config_parser().get('DEFAULT', 'Sep')
        if len(text) >= 2 and text[0:len(sep)] == sep and text[-len(sep):] == sep:
            self.plainTextEdit.setPlainText(text[len(sep):-len(sep)])

    def __init__(self):
        # noinspection PyArgumentList
        super().__init__()

        self.init_window_flags()

        loadUi('ui/main.ui', self)

        # inject the event handler
        self.imgLabel.mouseMoveEvent = MethodType(mouseMoveEvent, self.imgLabel)

        if config_handler.get_config_parser().getboolean('DEFAULT', 'ListenToClip'):
            QApplication.clipboard().dataChanged.connect(self.load_from_clipboard)
