from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

import config_handler


class SettingsDialog(QDialog):
    def load_config(self):
        self.topCheckbox.setChecked(config_handler.get_config_parser().getboolean('DEFAULT', 'AlwaysTop'))
        self.listenCheckbox.setChecked(config_handler.get_config_parser().getboolean('DEFAULT', 'ListenToClip'))

        self.delaySpinBox.setValue(config_handler.get_config_parser().getint('DEFAULT', 'WaitTime'))

        if config_handler.get_config_parser().get('DEFAULT', 'Render') == 'CodeCogs':
            self.codecogsRadio.setChecked(True)
        elif config_handler.get_config_parser().get('DEFAULT', 'Render') == 'Zhihu':
            self.zhihuRadio.setChecked(True)
        else:
            raise ValueError('Unsupported render engine')

    def save_and_quit(self):
        config_handler.get_config_parser().set('DEFAULT', 'AlwaysTop', str(self.topCheckbox.isChecked()))
        config_handler.get_config_parser().set('DEFAULT', 'ListenToClip', str(self.listenCheckbox.isChecked()))

        config_handler.get_config_parser().set('DEFAULT', 'WaitTime', str(self.delaySpinBox.value()))

        if self.codecogsRadio.isChecked():
            config_handler.get_config_parser().set('DEFAULT', 'Render', 'CodeCogs')
        elif self.zhihuRadio.isChecked():
            config_handler.get_config_parser().set('DEFAULT', 'Render', 'Zhihu')
        else:
            raise ValueError('Unknown radiobutton')
        config_handler.write_to_file()
        self.close()

    def __init__(self, parent=None):
        # noinspection PyArgumentList
        super(SettingsDialog, self).__init__(parent)

        loadUi('ui/settings.ui', self)
        self.load_config()
