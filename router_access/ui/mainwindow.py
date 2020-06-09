from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from .pages import loading, settings
from ..driver.main import DriverManager


class MainWindow(qtw.QMainWindow):

    def __init__(self,):
        super().__init__()

        self.driver_manager = DriverManager()

        self.initialize_UI()
        self.setup_widgets()

    def initialize_UI(self):
        self.setFixedSize(300, 650)
        self.setWindowTitle('Router - Settings')

        self.setWindowFlags(
            qtc.Qt.Dialog |
            qtc.Qt.CustomizeWindowHint |
            qtc.Qt.WindowTitleHint |
            qtc.Qt.WindowCloseButtonHint |
            qtc.Qt.WindowMinimizeButtonHint
        )

    def setup_widgets(self):
        self.loading_page = loading.LoadingPage()
        self.settings_page = settings.WlanSettingsPage(self.driver_manager)

        self.stacked_widget = qtw.QStackedWidget()
        self.stacked_widget.addWidget(self.loading_page)
        self.stacked_widget.addWidget(self.settings_page)

        self.setCentralWidget(self.stacked_widget)

    def next_page(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)
