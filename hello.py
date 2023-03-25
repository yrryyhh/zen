import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLCDNumber
from PIL import ImageFilter, Image, ImageQt
from qtpy import QtGui

import DigitalClock


class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2):
        self.radius = radius

    def filter(self, image):
        return image.gaussian_blur(self.radius)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.endPos = None
        self.startPos = None
        self.isPressed = None
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.palette = None
        self.main_widget = None
        self.initUi()

    def initUi(self):
        self.resize(800, 400)
        self.setWindowTitle('亚克力测试')
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        led_timer = DigitalClock.DigitalClock(self)
        led_timer.setMinimumSize(400, 100)
        layout.addWidget(led_timer)
        # self.lb.setStyleSheet('background-color: red;')
        self.setBackgroundImage()
        self.main_widget.setLayout(layout)

    def setBackgroundImage(self):
        path = r"C:\Users\20594\Desktop\总文件夹\css\001935-1615911575642b.jpg"
        img = Image.open(path)
        img = img.filter(MyGaussianBlur(radius=40))  # type: Image.Image
        if img.mode == "RGB":
            img = img.convert("RGBA")
        pixmap = ImageQt.toqpixmap(img)
        pixmap = pixmap.scaled(self.size().width(), self.size().width(), aspectRatioMode=Qt.KeepAspectRatio)
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(self.palette)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.setBackgroundImage()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_Space:
            self.close()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self.isPressed = True
            self.startPos = a0.globalPos()
            self.setCursor(Qt.SizeAllCursor)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.isPressed:
            self.endPos = a0.globalPos()
            self.move(self.endPos - self.startPos + self.pos())
            self.startPos = self.endPos
            self.update()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.isPressed = False
        self.setCursor(Qt.ArrowCursor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
