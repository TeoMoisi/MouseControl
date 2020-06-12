# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QFrame, QLabel, QGridLayout, QHBoxLayout
from Capture import Capture
from PyQt5.QtGui import QPixmap
from Constants import Constants

class SideMenu(QWidget):
    def __init__(self, splitter, parent=None):
        super(SideMenu, self).__init__(parent)
        self.capture = Capture()
        self._constants = Constants()
        self._splitter = splitter
        self._init_menu_buttons()

    def _init_menu_buttons(self):
        left = QFrame(self._splitter)
        left.setFrameShape(QFrame.StyledPanel)
        left.setFixedWidth(150)
        left.setStyleSheet("background-color: #a3c2c2; border: none; border-radius: 5px;")

        iconLabel = QLabel(left)
        pixmap = QPixmap(self._constants.logo_icon)
        iconLabel.setPixmap(pixmap.scaledToWidth(100))
        iconLabel.setContentsMargins(20, 0, 0, 0)
        iconLabel.resize(150, 50)

        self.start_button = QPushButton('Start', left)
        self.start_button.resize(150, 50)
        self.start_button.move(0, 50)
        self.start_button.setStyleSheet(open('style.css').read())
        self.start_button.setProperty('class', 'buttons')

        self.end_button = QPushButton('End', left)
        self.end_button.resize(150, 50)
        self.end_button.move(0, 100)
        self.end_button.setStyleSheet(open('style.css').read())
        self.end_button.setProperty('class', 'buttons')

        self.quit_button = QPushButton('Quit', left)
        self.quit_button.resize(150, 50)
        self.quit_button.move(0, 150)
        self.quit_button.setStyleSheet(open('style.css').read())
        self.quit_button.setProperty('class', 'buttons')

        self.check_box = QCheckBox("Hide landmarks", left)
        self.check_box.setStyleSheet(open('style.css').read())
        self.check_box.setProperty('class', 'checkbox')
        self.check_box.setChecked(False)
        self.check_box.resize(150, 50)
        self.check_box.move(15, 250)

        self._splitter.addWidget(left)
