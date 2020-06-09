from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from ..widgets.waiting_spinner import QtWaitingSpinner


class LoadingPage(qtw.QWidget):

    def __init__(self):
        super().__init__()

        self.setup_widgets()

    def setup_widgets(self):
        self.spinning_circle = self.create_spinning_circle()
        self.wait_label = self.create_wait_label()

        self.setLayout(qtw.QVBoxLayout())

        self.layout().addWidget(self.spinning_circle)
        self.layout().addWidget(self.wait_label)

    @staticmethod
    def create_spinning_circle():
        circle_properties = {'mNumberOfLines': 240, 'mInnerRadius': 40, 'mLineLength': 4}
        spinning_circle = QtWaitingSpinner()
        spinning_circle.setProperties(**circle_properties)

        spinning_circle.start()

        return spinning_circle

    @staticmethod
    def create_wait_label():
        wait_label = qtw.QLabel('Please wait', font=qtg.QFont('Arial', 14))
        wait_label.setAlignment(qtc.Qt.AlignCenter)

        return wait_label
