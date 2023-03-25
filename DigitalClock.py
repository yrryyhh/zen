from PyQt5 import QtGui
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtWidgets import QApplication, QLCDNumber


class DigitalClock(QLCDNumber):

    def __init__(self, parent=None):
        self.window_move_flag = False
        super(DigitalClock, self).__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setSegmentStyle(QLCDNumber.Outline)
        self.setStyleSheet('border: 0px solid red;')
        self.setDigitCount(8)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.resize(400, 100)
        self.showTime()

        # self.setWindowTitle("Digital Clock")

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm:ss')
        if (time.second() % 2) == 0:
            h, m, s = text.split(':')
            text = ' '.join([h, m, s])
        self.display(text)
