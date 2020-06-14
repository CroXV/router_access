from PyQt5 import QtCore as qtc


class Signals(qtc.QObject):

    result = qtc.pyqtSignal(object)
    finished = qtc.pyqtSignal()


class Worker(qtc.QRunnable):

    threadpool = qtc.QThreadPool()

    def __init__(self, fn, *args, **kwargs):
        super().__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            pass
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
