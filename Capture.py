# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
import cv2
from imutils import face_utils
import imutils
import numpy as np
from DetectMoves import DetectMoves
from MeasureUtils import MeasureUtils
from Constants import Constants
import pyautogui as pag
import dlib


class Capture():
    def __init__(self):
        self.capturing = False
        self.camera = cv2.VideoCapture(0)
        self._constants = Constants()
        self._detector = dlib.get_frontal_face_detector()
        self._predictor = dlib.shape_predictor(self._constants.shape_predictor)
        self._movesDetector = DetectMoves()
        self._measureUtils = MeasureUtils()
        self.input_mode = False
        self.scroll_mode = False
        self.landmarks_on = True

    def showLandmarks(self, frame):
        frame = imutils.resize(frame, width=self._constants.CAM_W, height=self._constants.CAM_H)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = self._detector(gray, 0)

        if len(rects) > 0:
            rect = rects[0]
            self.input_mode = True

            shape = self._predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            mouth = shape[self._constants.mStart:self._constants.mEnd]
            leftEye = shape[self._constants.lStart:self._constants.lEnd]
            rightEye = shape[self._constants.rStart:self._constants.rEnd]
            nose = shape[self._constants.nStart:self._constants.nEnd]

            temp = leftEye
            leftEye = rightEye
            rightEye = temp
            nose_point = (nose[3, 0], nose[3, 1])

            mouthHull = cv2.convexHull(mouth)
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            noseHull = cv2.convexHull(nose)

            if (self.landmarks_on):
                cv2.drawContours(frame, [mouthHull], -1, self._constants.YELLOW_COLOR, 1)
                cv2.drawContours(frame, [leftEyeHull], -1, self._constants.YELLOW_COLOR, 1)
                cv2.drawContours(frame, [rightEyeHull], -1, self._constants.YELLOW_COLOR, 1)
                cv2.drawContours(frame, [noseHull], -1, self._constants.YELLOW_COLOR, 1)

                for (x, y) in np.concatenate((mouth, leftEye, rightEye, nose), axis=0):
                    cv2.circle(frame, (x, y), 2, self._constants.GREEN_COLOR, -1)

            if self.input_mode:
                cv2.putText(frame, "Face detected! You can start to control your cursor.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self._constants.RED_COLOR, 2)
                x, y = self._constants.ANCHOR_POINT
                nx, ny = nose_point
                multiple = 1
                cv2.rectangle(frame, (x - self._constants.WIDTH, y - self._constants.HEIGHT), (x + self._constants.WIDTH, y + self._constants.HEIGHT), self._constants.GREEN_COLOR, 2)
                cv2.line(frame, self._constants.ANCHOR_POINT, nose_point, self._constants.BLUE_COLOR, 2)

                self._movesDetector.detectBlinkCos(leftEye, rightEye)

                self.scroll_mode = self._movesDetector.detectScroll(self.scroll_mode, mouth)

                dir = self._measureUtils.direction(nose_point, (x, y), self._constants.WIDTH, self._constants.HEIGHT)
                cv2.putText(frame, dir.upper(), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self._constants.RED_COLOR, 2)
                if dir == 'right':
                    pag.moveRel(self._constants.DRAG_MOTION, 0)
                elif dir == 'left':
                    pag.moveRel(-self._constants.DRAG_MOTION, 0)
                elif dir == 'up':
                    if self.scroll_mode:
                        pag.scroll(20)
                    else:
                        pag.moveRel(0, -self._constants.DRAG_MOTION)
                elif dir == 'down':
                    if self.scroll_mode:
                        pag.scroll(-20)
                    else:
                        pag.moveRel(0, self._constants.DRAG_MOTION)

            if self.scroll_mode:
                cv2.putText(frame, 'SCROLL MODE IS ON!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self._constants.RED_COLOR, 2)
            cv2.imshow("Capture", frame)

        else:
            cv2.imshow("Capture", frame)
            key = cv2.waitKey(1) & 0xFF

    def startCapture(self):
        print("pressed start")
        self.capturing = True
        while(self.capturing):
            ret, frame = self.camera.read()
            frame = cv2.flip(frame, 1)
            self.showLandmarks(frame)
            cv2.waitKey(5)
        cv2.destroyAllWindows()

    def endCapture(self):
        print("pressed End")
        self.capturing = False
        cv2.destroyAllWindows()
        self.camera.release()

    def hideLandmarks(self, checkBox):
        if checkBox.isChecked():
            self.landmarks_on = False
        else:
            self.landmarks_on = True
