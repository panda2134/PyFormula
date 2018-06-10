from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from about_window import AboutWindow
from settings_window import SettingsWindow


class MainWindow(QMainWindow):
    @staticmethod
    def show_about():
        AboutWindow().exec()

    @staticmethod
    def show_settings():
        SettingsWindow().exec()

    def __init__(self):
        super(MainWindow, self).__init__()

        loadUi('ui/main.ui', self)
