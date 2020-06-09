from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from ..mainwindow import MainWindow

from ..utils import manage_data
from router_access.ui.utils.worker import Worker
from ...driver.main import DriverManager


class LogInDialog(qtw.QDialog):

    authenticated = qtc.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.initialize_UI()
        self.intialize_driver()

        self.load_login()

    def initialize_UI(self):
        self.setFixedSize(250, 120)
        self.setWindowTitle('Router - Login')
        self.setWindowFlags(
            qtc.Qt.Dialog |
            qtc.Qt.CustomizeWindowHint |
            qtc.Qt.WindowTitleHint |
            qtc.Qt.WindowMinimizeButtonHint
        )

        self.setup_widgets()

    def intialize_driver(self):
        self.driver_loaded = False
        self.driver_manager = DriverManager()
        self.driver = Worker(self.driver_manager.driver.start_driver)
        self.driver.signals.finished.connect(self.update_driver)
        Worker.threadpool.start(self.driver)

    def update_driver(self):
        self.driver_loaded = True

    def setup_widgets(self):
        self.username_edit = qtw.QLineEdit(returnPressed=self.authenticate)
        self.password_edit = qtw.QLineEdit(returnPressed=self.authenticate,
                                           echoMode=qtw.QLineEdit.Password)
        self.save_login_checkbox = qtw.QCheckBox('Remember me?')

        self.cancel_button = qtw.QPushButton('Cancel', clicked=self.close)
        self.submit_button = qtw.QPushButton('Log In', clicked=self.authenticate)

        layout = qtw.QFormLayout()
        layout.addRow('Username', self.username_edit)
        layout.addRow('Password', self.password_edit)
        layout.addRow('', self.save_login_checkbox)

        hlayout = qtw.QHBoxLayout()
        hlayout.layout().addWidget(self.cancel_button)
        hlayout.layout().addWidget(self.submit_button)

        layout.addRow('', hlayout)

        self.setLayout(layout)

    def load_login(self):
        login_info = Worker(manage_data.retrieve_login)
        login_info.signals.result.connect(self.update_login)
        login_info.signals.finished.connect(self.show)
        Worker.threadpool.start(login_info)

    def update_login(self, login):
        usr, pwd = login

        if usr and pwd:
            self.username_edit.setText(usr)
            self.password_edit.setText(pwd)
            self.save_login_checkbox.setChecked(True)

    def save_login(self, usr, pwd):
        if self.save_login_checkbox.isChecked():
            login = Worker(manage_data.save_login(usr, pwd))
        else:
            login = Worker(manage_data.save_login('', ''))
        Worker.threadpool.start(login)

    def log_in_usr(self, usr, pwd):
        log_in = Worker(self.driver_manager.login_page.log_in, usr, pwd)
        log_in.signals.finished.connect(self.mw.next_page)

        if self.driver_loaded:
            Worker.threadpool.start(log_in)
        else:
            self.driver.signals.finished.connect(lambda: self.log_in_usr(usr, pwd))

    def authenticate(self):
        usr = self.username_edit.text()
        pwd = self.password_edit.text()

        if usr and pwd:
            self.authenticated.connect(self.show_main_window)
            self.authenticated.connect(self.save_login)
            self.authenticated.connect(self.log_in_usr)

            self.authenticated.emit(usr, pwd)

    def show_main_window(self):
        self.mw = MainWindow()

        self.close()
        self.mw.show()
