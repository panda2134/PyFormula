import os
import sys
import main_window
from portalocker import lock, LOCK_EX, unlock
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication

lockfile_name = 'pyformula.lck'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = main_window.MainWindow()

    if os.path.exists(lockfile_name):
        QMessageBox.warning(win, "Warning", \
'''
You have opened a window of PyFormula.
If not, please delete the \'pyformula.lck\' file.
''')
    else:
        with open(lockfile_name, 'w') as lockfile:
            lock(lockfile, LOCK_EX)
            win.show()
            return_code = app.exec()
            unlock(lockfile)

        os.remove(lockfile_name)
        sys.exit(return_code)
