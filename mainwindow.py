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
import cv2
import dlib
from imutils import face_utils
import imutils
import numpy as np
from DetectMoves import DetectMoves
import pyautogui as pag
from MeasureUtils import MeasureUtils
from Constants import Constants
from PyQt5 import QtGui
from Capture import Capture


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle('Facial Cursor')
        self.setWindowIcon(QtGui.QIcon("/Users/teofanamoisi/Desktop/icon.png"))
        self.initUI()

    def startDemo(self):

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()

        #create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        filename = "/Users/teofanamoisi/Desktop/ImaginiLicenta/Demo.mov"
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
        self.playBtn.setEnabled(True)

        #create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)

        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)

        #set widgets to the hbox layout
        #hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)


        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)


        self.rightLayout.addLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)


    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())

    def startVideo(self):
        VideoHandler(self.rightLayout).init_ui()

    def quitApp(self):
        print("pressed Quit")
        QApplication.quit()

    def initUI(self):
        hbox = QHBoxLayout(self)
        splitter1 = QSplitter(self)
        splitter1.setOrientation(Qt.Horizontal)

        left = QFrame(splitter1)
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

        right = QFrame(splitter1)
        right.setFrameShape(QFrame.StyledPanel)
        right.setStyleSheet("background-color: white; border: none; border-radius: 5px;")

        self.rightLayout = QHBoxLayout(right)

        #add buttons
        self.capture = Capture()
        self.startDemo()

        self.start_button = QPushButton('Start', left)
        self.start_button.resize(150, 50)
        self.start_button.move(0, 50)
        self.start_button.clicked.connect(self.capture.startCapture)
        self.start_button.setStyleSheet(open('styleButtons.css').read())
        self.start_button.setObjectName('firstButton')
        self.start_button.setProperty('class', 'generalButtons')

        self.end_button = QPushButton('End', left)
        self.end_button.clicked.connect(self.capture.endCapture)
        self.end_button.resize(150, 50)
        self.end_button.move(0, 100)
        self.end_button.setStyleSheet(open('styleButtons.css').read())
        self.end_button.setProperty('class', 'generalButtons')
        self.end_button.setProperty('id', 'endID')

        self.quit_button = QPushButton('Quit', left)
        self.quit_button.clicked.connect(self.quitApp)
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

        splitter1.addWidget(left)
        splitter1.addWidget(right)
        hbox.addWidget(splitter1)

        self.setGeometry(10, 50, 850, 450)

        self.setLayout(hbox)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setStyleSheet("background-color: #F7F4F2;")
    sys.exit(app.exec_())
