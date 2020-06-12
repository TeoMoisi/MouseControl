# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from Constants import Constants


class DemoPlayer(QWidget):
    def __init__(self, splitter, parent=None):
        super(DemoPlayer, self).__init__(parent)
        self._constants = Constants()
        self._splitter = splitter
        self._init_demo_player()

    def _init_demo_player(self):
        self.right = QFrame(self._splitter)
        self.right.setFrameShape(QFrame.StyledPanel)
        self.right.setStyleSheet("background-color: white; border: none; border-radius: 5px;")
        self.rightLayout = QHBoxLayout(self.right)

        self._start_demo()
        self._splitter.addWidget(self.right)

    def _start_demo(self):

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()

        #create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self._play_video)

        filename = self._constants.demo_filename
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
        self.playBtn.setEnabled(True)

        #create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self._set_position)

        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)

        #set widgets to the hbox layout
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)

        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)


        self.rightLayout.addLayout(vboxLayout)
        self.mediaPlayer.setVideoOutput(videowidget)

        self.mediaPlayer.stateChanged.connect(self._mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self._position_changed)
        self.mediaPlayer.durationChanged.connect(self._duration_changed)

    def _play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def _mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def _position_changed(self, position):
        self.slider.setValue(position)

    def _duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def _set_position(self, position):
        self.mediaPlayer.setPosition(position)
