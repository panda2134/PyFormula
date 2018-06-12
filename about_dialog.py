from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5.uic import loadUi


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)

        loadUi('ui/about.ui', self)
