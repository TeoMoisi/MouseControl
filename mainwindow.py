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
        self.initUI()

    def quitApp(self):
        print("pressed Quit")
        QApplication.quit()

    def initUI(self):
        hbox = QHBoxLayout(self)
        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Horizontal)

        self.capture = Capture()

        self.sideMenu = SideMenu(splitter, self)
        self.sideMenu.start_button.clicked.connect(self.capture.startCapture)
        self.sideMenu.end_button.clicked.connect(self.capture.endCapture)
        self.sideMenu.quit_button.clicked.connect(self.quitApp)
        self.sideMenu.checkBox.stateChanged.connect(lambda:self.capture.hideLandmarks(self.sideMenu.checkBox))

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
