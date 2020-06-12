# This Python file uses the following encoding: utf-8
import sys
import os
# from PySide2.QtWidgets import QApplication
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5 import QtGui
from Capture import Capture
from SideMenu import SideMenu
from DemoPlayer import DemoPlayer


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Facial Cursor')
        self._init_ui()

    def __quit_app(self):
        print("pressed Quit")
        QApplication.quit()

    def __start_capture(self):
        print("Start capture")
        self.capture = Capture()
        self.capture.startCapture()

    def __end_capture(self):
        if self.capture == None:
            return
        else:
            self.capture.endCapture()

    def __hide_landmarks(self):
        if self.capture == None:
            return
        else:
            return self.capture.hideLandmarks(self.sideMenu.check_box)

    def _init_ui(self):
        hbox = QHBoxLayout(self)
        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Horizontal)

        self.capture = None

        self.sideMenu = SideMenu(splitter, self)
        self.sideMenu.start_button.clicked.connect(self.__start_capture)
        self.sideMenu.end_button.clicked.connect(self.__end_capture)
        self.sideMenu.quit_button.clicked.connect(self.__quit_app)
        self.sideMenu.check_box.stateChanged.connect(lambda:self.__hide_landmarks())

        self.demoPlayer = DemoPlayer(splitter, self)

        hbox.addWidget(splitter)
        self.setGeometry(10, 50, 850, 450)
        self.setLayout(hbox)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setStyleSheet("background-color: #F7F4F2;")
    sys.exit(app.exec_())
