import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from loading import QtWaitingSpinner
from router_access.connections import Browser
from router_access.misc import save_login, retrieve_login


class Signals(qtc.QObject):

    started = qtc.pyqtSignal()
    result = qtc.pyqtSignal(object)
    finished = qtc.pyqtSignal()


class Worker(qtc.QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()

    def run(self):
        try:
            self.signals.started.emit()
            result = self.fn(*self.args, **self.kwargs)
        except:
            pass
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class LoginScreen(qtw.QDialog):

    authenticated = qtc.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.initialize_UI()

    def initialize_UI(self):
        self.setFixedSize(250, 120)
        self.setWindowTitle('Router - Login')
        self.setWindowFlags(
            qtc.Qt.Dialog |
            qtc.Qt.CustomizeWindowHint |
            qtc.Qt.WindowTitleHint |
            qtc.Qt.WindowMinimizeButtonHint
        )

        self.threadpool = qtc.QThreadPool()

        self.setup_widgets()
        self.setup_browser()

        self.main = MainWindow(browser=self.browser, threadpool=self.threadpool)

    def setup_widgets(self):
        self.build_user()
        self.cancel_button = qtw.QPushButton('Cancel', clicked=self.close)
        self.submit_button = qtw.QPushButton('Login', clicked=self.authenticate)

        layout = qtw.QFormLayout()
        layout.addRow('Username', self.username_edit)
        layout.addRow('Password', self.password_edit)
        layout.addRow('', self.save_login_checkbox)

        hlayout = qtw.QHBoxLayout()
        hlayout.layout().addWidget(self.cancel_button)
        hlayout.layout().addWidget(self.submit_button)

        layout.addRow('', hlayout)

        self.setLayout(layout)

        self.authenticated.connect(self.handle_login_info)
        self.authenticated.connect(self.handle_auth_result)

    def build_user(self):
        self.username_edit = qtw.QLineEdit(returnPressed=self.authenticate)
        self.password_edit = qtw.QLineEdit(returnPressed=self.authenticate,
                                           echoMode=qtw.QLineEdit.Password)
        self.save_login_checkbox = qtw.QCheckBox('Remember me?')

        login_info = Worker(retrieve_login)
        login_info.signals.result.connect(self.update_login_info)
        login_info.signals.finished.connect(self.show)
        self.threadpool.start(login_info)

    def update_login_info(self, login_info):
        username, password = login_info

        if username and password:
            self.username_edit.setText(username)
            self.password_edit.setText(password)
            self.save_login_checkbox.setChecked(True)

    def authenticate(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        if username and password:
            self.close()
            self.main.show()

            self.authenticated.emit(username, password)

    def handle_login_info(self, username, password):
        if self.save_login_checkbox.checkState() != qtc.Qt.Checked:
            username, password = '', ''

        save_info = Worker(save_login, username, password)
        self.threadpool.start(save_info)

    def handle_auth_result(self, username, password):
        login = Worker(self.browser.login, username, password)
        login.signals.finished.connect(self.main.next_page)

        if self.login_page_loaded:
            self.threadpool.start(login)
        else:
            self.driver.signals.finished.connect(lambda: self.threadpool.start(login))

    def setup_browser(self):
        self.browser = Browser()
        self.login_page_loaded = False

        # Start driver on a different thread
        self.driver = Worker(self.browser.start_driver)
        self.driver.signals.finished.connect(self.update_page_status)

        self.threadpool.start(self.driver)

    def update_page_status(self):
        self.login_page_loaded = True


class MainWindow(qtw.QMainWindow):

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update((k, v) for k, v in kwargs.items())
        self.initialize_UI()

    def initialize_UI(self):
        self.setFixedSize(350, 650)
        self.setWindowTitle('Router - Settings')

        self.setWindowFlags(
            qtc.Qt.Dialog |
            qtc.Qt.CustomizeWindowHint |
            qtc.Qt.WindowTitleHint |
            qtc.Qt.WindowCloseButtonHint |
            qtc.Qt.WindowMinimizeButtonHint
        )

        self.setup_widgets()

    def setup_widgets(self):
        self.setup_loading_circle()
        self.setup_wlan_widget()

        self.stacked_widget = qtw.QStackedWidget()
        self.stacked_widget.addWidget(self.loading_circle)
        self.stacked_widget.addWidget(self.wlan_widget)

        self.setCentralWidget(self.stacked_widget)

    def setup_loading_circle(self):
        properties = {'mNumberOfLines': 150, 'mInnerRadius': 50, 'mLineLength': 5}
        self.loading_circle = QtWaitingSpinner()
        self.loading_circle.changeCircleProperties(**properties)
        self.loading_circle.start()

    def setup_wlan_widget(self):
        self.wlan_widget = qtw.QWidget()

        self.status_label = qtw.QLabel('Hi', font=qtg.QFont('Sans', 25, qtg.QFont.Bold))
        self.wifi_toggle_button = qtw.QPushButton('Router XS', clicked=self.handle_wifi_toggle)

        self.wlan_widget.setLayout(qtw.QVBoxLayout())
        self.wlan_widget.layout().addWidget(self.status_label, alignment=qtc.Qt.AlignHCenter)
        self.wlan_widget.layout().addWidget(self.wifi_toggle_button)

    def next_page(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)

    def handle_wifi_toggle(self):
        self.wifi_toggle_button.disconnect()

        self.status_label.setText('Toggling Wifi...')
        toggle = Worker(self.browser.toggleWifi)
        toggle.signals.finished.connect(self.wifi_toggle_finished)

        self.threadpool.start(toggle)

    def wifi_toggle_finished(self):
        self.wifi_toggle_button.clicked.connect(self.handle_wifi_toggle)
        self.status_label.setText('Done.')


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    win = LoginScreen()
    app.aboutToQuit.connect(win.browser.quit_driver)
    sys.exit(app.exec_())
