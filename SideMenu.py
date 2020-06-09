# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QFrame, QLabel, QGridLayout, QHBoxLayout
from Capture import Capture
from PyQt5.QtGui import QPixmap

class SideMenu(QWidget):
    def __init__(self, splitter, parent=None):
        super(SideMenu, self).__init__(parent)
        self.capture = Capture()
        self.splitter = splitter
        self.init_menu_buttons()

    def init_menu_buttons(self):
        left = QFrame(self.splitter)
        left.setFrameShape(QFrame.StyledPanel)
        left.setMaximumWidth(200)
        left.setMinimumWidth(150)
        left.setStyleSheet("background-color: #a3c2c2; border: none; border-radius: 5px;")

        iconLabel = QLabel(left)
        pixmap = QPixmap("/Users/teofanamoisi/Desktop/icon.png")
        iconLabel.setPixmap(pixmap.scaledToWidth(150))
        iconLabel.resize(150, 50)

        self.leftLayout = QHBoxLayout(left)
        self.gridLayout = QGridLayout()

        self.start_button = QPushButton('Start', left)
        self.start_button.resize(150, 50)
        self.start_button.move(0, 50)
        #self.start_button.clicked.connect(self.capture.startCapture)
        self.start_button.setStyleSheet(open('styleButtons.css').read())
        self.start_button.setObjectName('firstButton')
        self.start_button.setProperty('class', 'generalButtons')

        self.end_button = QPushButton('End', left)
        #self.end_button.clicked.connect(self.capture.endCapture)
        self.end_button.resize(150, 50)
        self.end_button.move(0, 100)
        self.end_button.setStyleSheet(open('styleButtons.css').read())
        self.end_button.setProperty('class', 'generalButtons')
        self.end_button.setProperty('id', 'endID')

        self.quit_button = QPushButton('Quit', left)
        #self.quit_button.clicked.connect(self.quitApp)
        self.quit_button.resize(150, 50)
        self.quit_button.move(0, 150)
        self.quit_button.setStyleSheet(open('styleButtons.css').read())
        self.quit_button.setProperty('class', 'generalButtons')
        self.quit_button.setProperty('id', 'quitID')

        self.checkBox = QCheckBox("Hide landmarks", left)
        self.checkBox.setChecked(False)
        self.checkBox.resize(150, 50)
        self.checkBox.move(0, 250)
        self.checkBox.stateChanged.connect(lambda:self.capture.hideLandmarks(self.checkBox))

        self.leftLayout.addLayout(self.gridLayout)

        self.splitter.addWidget(left)
