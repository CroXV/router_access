from math import ceil

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QtWaitingSpinner(QWidget):

    def __init__(self):
        super().__init__()

        self.drawCircle = False
        self.defaultCircleValues()

    def defaultCircleValues(self):
        self.mCenterOnParent = True
        self.mDisableParentWhenSpinning = False

        self.mColor = QColor(Qt.black)
        self.mRoundness = 100.0
        self.mMinimumTrailOpacity = 31.4159265358979323846
        self.mTrailFadePercentage = 50.0
        self.mRevolutionsPerSecond = 1.57079632679489661923
        self.mNumberOfLines = 20
        self.mLineLength = 10
        self.mLineWidth = 2
        self.mInnerRadius = 20
        self.mCurrentCounter = 0
        self.mIsSpinning = False

    def changeCircleProperties(self, **kwargs):
        properties = {
            'mCenterOnParent',
            'mDisableParentWhenSpinning',
            'mColor',
            'mRoundness',
            'mMinimumTrailOpacity',
            'mTrailFadePercentage',
            'mRevolutionsPerSecond',
            'mNumberOfLines',
            'mLineLength',
            'mLineWidth',
            'mInnerRadius',
            'mCurrentCounter',
            'mIsSpinning'
        }

        self.__dict__.update((key, value) for key, value in kwargs.items() if key in properties)

    def initialize(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.updateSize()
        self.updateTimer()

    def start(self):
        self.initialize()
        self.updatePosition()

        self.mIsSpinning = True
        self.drawCircle = True

        if self.parentWidget() and self.mDisableParentWhenSpinning:
            self.parentWidget().setEnabled(False)

        if not self.timer.isActive():
            self.timer.start()
            self.mCurrentCounter = 0

    def stop(self):
        self.mIsSpinning = False
        self.drawCircle = False

        if self.parentWidget() and self.mDisableParentWhenSpinning:
            self.parentWidget().setEnabled(True)

        if self.timer.isActive():
            self.timer.stop()
            self.mCurrentCounter = 0

    @pyqtSlot()
    def rotate(self):
        self.mCurrentCounter += 1
        if self.mCurrentCounter > self.numberOfLines():
            self.mCurrentCounter = 0
        self.update()

    def updateSize(self):
        size = (self.mInnerRadius + self.mLineLength) * 2
        self.setFixedSize(size, size)

    def updateTimer(self):
        self.timer.setInterval(int(1000 / (self.mNumberOfLines * self.mRevolutionsPerSecond)))

    def updatePosition(self):
        if self.parentWidget() and self.mCenterOnParent:
            self.move(int(self.parentWidget().width() / 2 - self.width() / 2),
                      int(self.parentWidget().height() / 2 - self.height() / 2))

    def lineCountDistanceFromPrimary(self, current, primary, totalNrOfLines):
        distance = primary - current
        if distance < 0:
            distance += totalNrOfLines
        return distance

    def currentLineColor(self, countDistance, totalNrOfLines, trailFadePerc, minOpacity, color):
        if countDistance == 0:
            return color

        minAlphaF = minOpacity / 100.0

        distanceThreshold = ceil((totalNrOfLines - 1) * trailFadePerc / 100.0)
        if countDistance > distanceThreshold:
            color.setAlphaF(minAlphaF)

        else:
            alphaDiff = self.mColor.alphaF() - minAlphaF
            gradient = alphaDiff / distanceThreshold + 1.0
            resultAlpha = color.alphaF() - gradient * countDistance
            resultAlpha = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(resultAlpha)
        return color

    def paintEvent(self, event):
        if self.drawCircle:
            self.updatePosition()
            painter = QPainter(self)
            painter.fillRect(self.rect(), Qt.transparent)
            painter.setRenderHint(QPainter.Antialiasing, True)
            if self.mCurrentCounter > self.mNumberOfLines:
                self.mCurrentCounter = 0
            painter.setPen(Qt.NoPen)

            for i in range(self.mNumberOfLines):
                painter.save()
                painter.translate(self.mInnerRadius + self.mLineLength,
                                  self.mInnerRadius + self.mLineLength)
                rotateAngle = 360.0 * i / self.mNumberOfLines
                painter.rotate(rotateAngle)
                painter.translate(self.mInnerRadius, 0)
                distance = self.lineCountDistanceFromPrimary(i, self.mCurrentCounter,
                                                             self.mNumberOfLines)
                color = self.currentLineColor(distance, self.mNumberOfLines,
                                              self.mTrailFadePercentage, self.mMinimumTrailOpacity, self.mColor)
                painter.setBrush(color)
                painter.drawRoundedRect(QRect(0, -self.mLineWidth // 2, self.mLineLength, self.mLineLength),
                                        self.mRoundness, Qt.RelativeSize)
                painter.restore()

    def setNumberOfLines(self, lines):
        self.mNumberOfLines = lines
        self.updateTimer()

    def setLineLength(self, length):
        self.mLineLength = length
        self.updateSize()

    def setLineWidth(self, width):
        self.mLineWidth = width
        self.updateSize()

    def setInnerRadius(self, radius):
        self.mInnerRadius = radius
        self.updateSize()

    def color(self):
        return self.mColor

    def roundness(self):
        return self.mRoundness

    def minimumTrailOpacity(self):
        return self.mMinimumTrailOpacity

    def trailFadePercentage(self):
        return self.mTrailFadePercentage

    def revolutionsPersSecond(self):
        return self.mRevolutionsPerSecond

    def numberOfLines(self):
        return self.mNumberOfLines

    def lineLength(self):
        return self.mLineLength

    def lineWidth(self):
        return self.mLineWidth

    def innerRadius(self):
        return self.mInnerRadius

    def isSpinning(self):
        return self.mIsSpinning

    def setRoundness(self, roundness):
        self.mRoundness = min(0.0, max(100, roundness))

    def setColor(self, color):
        self.mColor = color

    def setRevolutionsPerSecond(self, revolutionsPerSecond):
        self.mRevolutionsPerSecond = revolutionsPerSecond
        self.updateTimer()

    def setTrailFadePercentage(self, trail):
        self.mTrailFadePercentage = trail

    def setMinimumTrailOpacity(self, minimumTrailOpacity):
        self.mMinimumTrailOpacity = minimumTrailOpacity
