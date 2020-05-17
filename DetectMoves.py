# This Python file uses the following encoding: utf-8
from MeasureUtils import MeasureUtils
from Constants import Constants
import numpy as np
import pyautogui as pag
import cv2

class DetectMoves:
    def __init__(self):
        self.measureUtils = MeasureUtils()
        self.constants = Constants()
        self.EAR = 0.0
        self.diff_ear = None

    def detectBlink(self, leftEye, rightEye):
        leftEAR = self.measureUtils.eye_aspect_ratio(leftEye)
        rightEAR = self.measureUtils.eye_aspect_ratio(rightEye)
        rightCosin = self.measureUtils.measureCosin(rightEye)
        leftCosin = self.measureUtils.measureCosin(leftEye)
        self.EAR = (leftEAR + rightEAR) / 2.0
        self.diff_ear = np.abs(leftEAR - rightEAR)

        if self.diff_ear > self.constants.WINK_AR_DIFF_THRESH:
            if leftEAR > rightEAR:
                if rightCosin >= 0.82:
                    print("Cosin right", rightCosin)
                    self.constants.WINK_COUNTER += 1
#                if rightEAR < self.constants.EYE_AR_THRESH:
#                    print("Cosin right", rightCosin)
#                    self.constants.WINK_COUNTER += 1


                    if self.constants.WINK_COUNTER > self.constants.WINK_CONSECUTIVE_FRAMES:
                        pag.click(button='right')
                        self.constants.WINK_COUNTER = 0

            elif leftEAR < rightEAR:
                if leftCosin >= 0.82 :
                #if leftEAR < self.constants.EYE_AR_THRESH:
                    self.constants.WINK_COUNTER += 1
                    if self.constants.WINK_COUNTER > self.constants.WINK_CONSECUTIVE_FRAMES:
                        pag.click(button='left')
                        self.constants.WINK_COUNTER = 0
            else:
                self.constants.WINK_COUNTER = 0

    def detectScroll(self, scroll_mode, mouth):
        mar = self.measureUtils.mouth_aspect_ratio(mouth)
        if mar > self.constants.MOUTH_AR_THRESH:
            self.constants.MOUTH_COUNTER += 1

            if self.constants.MOUTH_COUNTER >= self.constants.MOUTH_AR_CONSECUTIVE_FRAMES:
                # if the alarm is not on, turn it on
                scroll_mode = not scroll_mode
                # SCROLL_MODE = not SCROLL_MODE
                self.constants.MOUTH_COUNTER = 0

        else:
            self.constants.MOUTH_COUNTER = 0

        return scroll_mode

    #def detectSwipe(self, eyebrow):

#    def moveCursor(self, nose, frame):
#        nose_point = (nose[3, 0], nose[3, 1])
#        x, y = self.ANCHOR_POINT
#        nx, ny = nose_point
#        w, h = 50, 35
#        multiple = 1
#        cv2.rectangle(frame, (x - w, y - h), (x + w, y + h), self.GREEN_COLOR, 2)
#        cv2.line(frame, self.ANCHOR_POINT, nose_point, self.BLUE_COLOR, 2)

#        dir = self.measureUtils.direction(nose_point, self.ANCHOR_POINT, w, h)
#        cv2.putText(frame, dir.upper(), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.RED_COLOR, 2)
#        drag = 18
#        if dir == 'right':
#            pag.moveRel(drag, 0)
#        elif dir == 'left':
#            pag.moveRel(-drag, 0)
#        elif dir == 'up':
#            pag.moveRel(0, -drag)
#        elif dir == 'down':
#            pag.moveRel(0, drag)
