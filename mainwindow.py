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
import threading

class Capture():
    def __init__(self):
        self.capturing = False
        self.c = cv2.VideoCapture(0)
        self.shape_predictor = "/Users/teofanamoisi/Desktop/LandmarksTrain/predictorMax.dat"
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.shape_predictor)
        self.movesDetector = DetectMoves()
        self.ANCHOR_POINT = (0, 0)
        self.measureUtils = MeasureUtils()
        self.constants = Constants()
        self.INPUT_MODE = False
        self.SCROLL_MODE = False

    def showLandmarks(self, frame):
        frame = imutils.resize(frame, width=self.constants.CAM_W, height=self.constants.CAM_H)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        rects = self.detector(gray, 0)
        print(len(rects))

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
            cv2.drawContours(frame, [mouthHull], -1, self.constants.YELLOW_COLOR, 1)
            cv2.drawContours(frame, [leftEyeHull], -1, self.constants.YELLOW_COLOR, 1)
            cv2.drawContours(frame, [rightEyeHull], -1, self.constants.YELLOW_COLOR, 1)
            cv2.drawContours(frame, [noseHull], -1, self.constants.YELLOW_COLOR, 1)

            for (x, y) in np.concatenate((mouth, leftEye, rightEye, nose), axis=0):
                cv2.circle(frame, (x, y), 2, self.constants.GREEN_COLOR, -1)

            #self.movesDetector.detectBlink(leftEye, rightEye)
            #self.SCROLL_MODE = self.movesDetector.detectScroll(self.SCROLL_MODE)
            #print(self.SCROLL_MODE)
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

            self.showLandmarks(frame)
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

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    capturing = False
    shape_predictor = "/Users/teofanamoisi/Desktop/LandmarksTrain/predictorMax.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)
    movesDetector = DetectMoves()
    ANCHOR_POINT = (0, 0)
    measureUtils = MeasureUtils()
    constants = Constants()
    INPUT_MODE = False
    SCROLL_MODE = False

    def showLandmarks(self, frame):
        frame = imutils.resize(frame, width=self.constants.CAM_W, height=self.constants.CAM_H)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        rects = self.detector(gray, 0)
        print(len(rects))

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
            cv2.drawContours(frame, [mouthHull], -1, self.constants.YELLOW_COLOR, 1)
            cv2.drawContours(frame, [leftEyeHull], -1, self.constants.YELLOW_COLOR, 1)
            cv2.drawContours(frame, [rightEyeHull], -1, self.constants.YELLOW_COLOR, 1)
            cv2.drawContours(frame, [noseHull], -1, self.constants.YELLOW_COLOR, 1)

            for (x, y) in np.concatenate((mouth, leftEye, rightEye, nose), axis=0):
                cv2.circle(frame, (x, y), 2, self.constants.GREEN_COLOR, -1)

            #self.movesDetector.detectBlink(leftEye, rightEye)
            #self.SCROLL_MODE = self.movesDetector.detectScroll(self.SCROLL_MODE)
            #print(self.SCROLL_MODE)
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

    def run(self):
        print("pressed start")
        self.capturing = True
        cap = cv2.VideoCapture(0)
        while(self.capturing):
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            frame = self.showLandmarks(frame)
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def stopCapture(self):
        self.capturing = False


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle('Menu')
        self.setStyleSheet("background-color: #F0F8FF;")
        #self.th = Thread(self)
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def startCapture(self):
        #th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

    def stopCapture(self):
        self.rightLayout.removeWidget(self.label)


    def initUI(self):
        self.th = Thread(self)
        self.resize(1800, 1200)
        # create a label
        self.label = QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)
#        th = Thread(self)
#        th.changePixmap.connect(self.setImage)
#        th.start()

        hbox = QHBoxLayout(self)
        splitter1 = QSplitter(self)
        splitter1.setOrientation(Qt.Horizontal)

        left = QFrame(splitter1)
        left.setFrameShape(QFrame.StyledPanel)
        left.setMaximumWidth(150)

        self.leftLayout = QHBoxLayout(left)
        self.gridLayout = QGridLayout()

        right = QFrame(splitter1)
        right.setFrameShape(QFrame.StyledPanel)
        right.setStyleSheet("background-color: grey;")

        self.rightLayout = QHBoxLayout(right)
        self.rightLayout.addWidget(self.label)

        #add buttons
        self.capture = Capture()
        self.start_button = QPushButton('Start', left)
        self.start_button.clicked.connect(self.startCapture)
        self.start_button.setStyleSheet(open('styleButtons.css').read())
        self.start_button.setObjectName('firstButton')
        self.start_button.setProperty('class', 'generalButtons')
        self.gridLayout.addWidget(self.start_button)

        self.end_button =QPushButton('End', self)
        self.end_button.clicked.connect(self.stopCapture)
        self.end_button.setStyleSheet(open('styleButtons.css').read())
        self.end_button.setProperty('class', 'generalButtons')
        self.gridLayout.addWidget(self.end_button)

        self.quit_button = QPushButton('Quit', self)
        self.quit_button.clicked.connect(self.capture.quitCapture)
        self.quit_button.setStyleSheet(open('styleButtons.css').read())
        self.quit_button.setProperty('class', 'generalButtons')
        self.gridLayout.addWidget(self.quit_button)

        self.leftLayout.addLayout(self.gridLayout)

        splitter1.addWidget(left)
        splitter1.addWidget(right)
        hbox.addWidget(splitter1)

        self.setGeometry(10, 50, 850, 420)

        self.setLayout(hbox)
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
