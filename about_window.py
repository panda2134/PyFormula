from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5.uic import loadUi


class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)

        loadUi('ui/about.ui', self)
