# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
import cv2
import dlib
from imutils import face_utils
import imutils
import numpy as np
from DetectMoves import DetectMoves
from MeasureUtils import MeasureUtils
from Constants import Constants
import pyautogui as pag


class Capture():
    def __init__(self):
        self.capturing = False
        self.c = cv2.VideoCapture(0)
        self.constants = Constants()
        self.shape_predictor = self.constants.shape_predictor
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.shape_predictor)
        self.movesDetector = DetectMoves()
        self.ANCHOR_POINT = (0, 0)
        self.measureUtils = MeasureUtils()
        self.INPUT_MODE = False
        self.SCROLL_MODE = False
        self.landmarks_on = True

    def showLandmarks(self, frame):
        frame = imutils.resize(frame, width=self.constants.CAM_W, height=self.constants.CAM_H)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 0)

        if len(rects) > 0:
            rect = rects[0]
            self.INPUT_MODE = True

            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            mouth = shape[self.constants.mStart:self.constants.mEnd]
            leftEye = shape[self.constants.lStart:self.constants.lEnd]
            rightEye = shape[self.constants.rStart:self.constants.rEnd]
            nose = shape[self.constants.nStart:self.constants.nEnd]

            temp = leftEye
            leftEye = rightEye
            rightEye = temp
            nose_point = (nose[3, 0], nose[3, 1])

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

                self.movesDetector.detectBlinkCos(leftEye, rightEye)

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

        else:
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

    def startCapture(self):
        print("pressed start")
        self.capturing = True
        while(self.capturing):
            ret, frame = self.c.read()
            frame = cv2.flip(frame, 1)
            self.showLandmarks(frame)
            cv2.waitKey(5)
        cv2.destroyAllWindows()

    def endCapture(self):
        print("pressed End")
        self.capturing = False
        cv2.destroyAllWindows()

    def hideLandmarks(self, checkBox):
        if checkBox.isChecked():
            self.landmarks_on = False
        else:
            self.landmarks_on = True
