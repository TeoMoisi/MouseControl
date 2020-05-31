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
from VideoWindow import VideoWindow
from VideoHandler import VideoHandler
from PyQt5 import QtGui

class Capture():
    def __init__(self):
        self.capturing = False
        self.c = cv2.VideoCapture(0)
        self.shape_predictor = "/Users/teofanamoisi/Desktop/TrainShapePredictor/predictorMax.dat"
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.shape_predictor)
        self.movesDetector = DetectMoves()
        self.ANCHOR_POINT = (0, 0)
        self.measureUtils = MeasureUtils()
        self.constants = Constants()
        self.INPUT_MODE = False
        self.SCROLL_MODE = False
        self.landmarks_on = True

    def showLandmarks(self, frame):
        frame = imutils.resize(frame, width=self.constants.CAM_W, height=self.constants.CAM_H)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        rects = self.detector(gray, 0)

        # Loop over the face detections
        if len(rects) > 0:
            rect = rects[0]
            self.INPUT_MODE = True

            # Determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # Extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            mouth = shape[self.constants.mStart:self.constants.mEnd]
            leftEye = shape[self.constants.lStart:self.constants.lEnd]
            rightEye = shape[self.constants.rStart:self.constants.rEnd]
            nose = shape[self.constants.nStart:self.constants.nEnd]

            temp = leftEye
            leftEye = rightEye
            rightEye = temp

            # Average the mouth aspect ratio together for both eyes

            nose_point = (nose[3, 0], nose[3, 1])

            # Compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            mouthHull = cv2.convexHull(mouth)
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            noseHull = cv2.convexHull(nose)

            if (self.landmarks_on):
                cv2.drawContours(frame, [mouthHull], -1, self.constants.YELLOW_COLOR, 1)
                cv2.drawContours(frame, [leftEyeHull], -1, self.constants.YELLOW_COLOR, 1)
                cv2.drawContours(frame, [rightEyeHull], -1, self.constants.YELLOW_COLOR, 1)
                cv2.drawContours(frame, [noseHull], -1, self.constants.YELLOW_COLOR, 1)

                for (x, y) in np.concatenate((mouth, leftEye, rightEye, nose), axis=0):
                    cv2.circle(frame, (x, y), 2, self.constants.GREEN_COLOR, -1)

            if self.INPUT_MODE:
                cv2.putText(frame, "Face detected! You can start to control your cursor.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.constants.RED_COLOR, 2)
                x, y = self.constants.ANCHOR_POINT
                nx, ny = nose_point
                multiple = 1
                cv2.rectangle(frame, (x - self.constants.WIDTH, y - self.constants.HEIGHT), (x + self.constants.WIDTH, y + self.constants.HEIGHT), self.constants.GREEN_COLOR, 2)
                cv2.line(frame, self.constants.ANCHOR_POINT, nose_point, self.constants.BLUE_COLOR, 2)

                self.movesDetector.detectBlink(leftEye, rightEye)

                self.SCROLL_MODE = self.movesDetector.detectScroll(self.SCROLL_MODE, mouth)

                dir = self.measureUtils.direction(nose_point, (x, y), self.constants.WIDTH, self.constants.HEIGHT)
                cv2.putText(frame, dir.upper(), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.constants.RED_COLOR, 2)
                if dir == 'right':
                    pag.moveRel(self.constants.DRAG_MOTION, 0)
                elif dir == 'left':
                    pag.moveRel(-self.constants.DRAG_MOTION, 0)
                elif dir == 'up':
                    if self.SCROLL_MODE:
                        pag.scroll(20)
                    else:
                        pag.moveRel(0, -self.constants.DRAG_MOTION)
                elif dir == 'down':
                    if self.SCROLL_MODE:
                        pag.scroll(-20)
                    else:
                        pag.moveRel(0, self.constants.DRAG_MOTION)


            if self.SCROLL_MODE:
                cv2.putText(frame, 'SCROLL MODE IS ON!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.constants.RED_COLOR, 2)

            cv2.imshow("Frame", frame)
            return frame
            #scroll_mode = self.movesDetector.detectBlink(leftEye, rightEye)

        else:
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF


    def startCapture(self):
        print("pressed start")
        self.capturing = True
        cap = self.c
        while(self.capturing):
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            frame = self.showLandmarks(frame)
            cv2.waitKey(5)
        cv2.destroyAllWindows()


    def endCapture(self):
        print("pressed End")
        self.capturing = False

    def quitCapture(self):
        print("pressed Quit")
        cap = self.c
        cv2.destroyAllWindows()
        cap.release()
        QApplication.quit()

    def hideLandmarks(self, checkBox):
       if checkBox.isChecked():
           self.landmarks_on = False
       else:
           self.landmarks_on = True


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle('Facial Cursor')
        self.setWindowIcon(QtGui.QIcon("/Users/teofanamoisi/Desktop/icon.png"))
        self.initUI()

    def startDemo(self):

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)


        #create videowidget object

        videowidget = QVideoWidget()


        #create open button
#        openBtn = QPushButton('Open Video')
#        openBtn.clicked.connect(self.open_file)

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


        #media player signals

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
        VideoHandler(self.rightLayout)

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
        self.start_button = QPushButton('Start', left)
        self.start_button.resize(150, 50)
        self.start_button.move(0, 50)
        self.start_button.clicked.connect(self.capture.startCapture)
        self.start_button.setStyleSheet(open('styleButtons.css').read())
        self.start_button.setObjectName('firstButton')
        self.start_button.setProperty('class', 'generalButtons')
        #self.gridLayout.addWidget(self.start_button)
        #self.start_button.resize(150, 50)

        self.startDemo()

        self.end_button = QPushButton('End', left)
        self.end_button.clicked.connect(self.capture.endCapture)
        self.end_button.resize(150, 50)
        self.end_button.move(0, 100)
        self.end_button.setStyleSheet(open('styleButtons.css').read())
        self.end_button.setProperty('class', 'generalButtons')
        self.end_button.setProperty('id', 'endID')
        #self.gridLayout.addWidget(self.end_button)

        self.quit_button = QPushButton('Quit', left)
        self.quit_button.clicked.connect(self.capture.quitCapture)
        self.quit_button.resize(150, 50)
        self.quit_button.move(0, 150)
        self.quit_button.setStyleSheet(open('styleButtons.css').read())
        self.quit_button.setProperty('class', 'generalButtons')
        self.quit_button.setProperty('id', 'quitID')
        #self.gridLayout.addWidget(self.quit_button, 150, 50)

        self.checkBox = QCheckBox("Hide landmarks", left)
        self.checkBox.setChecked(False)
        self.checkBox.resize(150, 50)
        self.checkBox.move(0, 250)
        self.checkBox.stateChanged.connect(lambda:self.capture.hideLandmarks(self.checkBox))
        #self.gridLayout.addWidget(self.checkBox)

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
