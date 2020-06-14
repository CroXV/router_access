from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from router_access.ui.utils.worker import Worker


class WlanSettingsPage(qtw.QWidget):

    status = qtc.pyqtSignal(str)

    def __init__(self, driver_manager):
        super().__init__()

        self.driver_manager = driver_manager
        self.settings = driver_manager.settings_page

        self.setup_widgets()

    def setup_widgets(self):
        self.status_label = qtw.QLabel('Hi', font=qtg.QFont('Arial', 25, qtg.QFont.Bold))

        self.wifi_toggle_button = qtw.QPushButton('Router XS', clicked=self.handle_wifi_toggle)

        self.setLayout(qtw.QVBoxLayout())
        self.layout().addWidget(self.status_label, alignment=qtc.Qt.AlignHCenter)
        self.layout().addWidget(self.wifi_toggle_button)

    def handle_wifi_toggle(self):
        self.wifi_toggle_button.disconnect()

        toggle = Worker(self.settings.toggle_wifi, status=self.status)
        toggle.signals.finished.connect(self.wifi_toggle_finished)
        Worker.threadpool.start(toggle)

        self.status.connect(self.status_update)

    def status_update(self, status):
        self.status_label.setFont(qtg.QFont('Arial', 20, qtg.QFont.Bold))
        self.status_label.setText(status)

    def wifi_toggle_finished(self):
        self.wifi_toggle_button.clicked.connect(self.handle_wifi_toggle)
