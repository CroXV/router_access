from PyQt5 import QtWidgets as qtw
from .ui.dialogs.login import LogInDialog


def run():
    app = qtw.QApplication([])
    win = LogInDialog()
    app.aboutToQuit.connect(win.driver_manager.driver.exit_driver)
    app.exec_()