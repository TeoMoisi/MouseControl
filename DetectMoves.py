# This Python file uses the following encoding: utf-8
from MeasureUtils import MeasureUtils
from Constants import Constants
import numpy as np
import pyautogui as pag
import cv2
import sys
import os

class DetectMoves:
    def __init__(self):
        self.measureUtils = MeasureUtils()
        self.constants = Constants()
        self.EAR = 0.0
        self.diff_ear = None

    def detectBlinkEAR(self, leftEye, rightEye):
        leftEAR = self.measureUtils.eye_aspect_ratio(leftEye)
        rightEAR = self.measureUtils.eye_aspect_ratio(rightEye)
        self.EAR = (leftEAR + rightEAR) / 2.0
        self.diff_ear = np.abs(leftEAR - rightEAR)

        if self.diff_ear > self.constants.WINK_AR_DIFF_THRESH:
            if rightEAR < leftEAR:
                if rightEAR < self.constants.EYE_AR_THRESH:
                    self.constants.WINK_COUNTER += 1

                    if self.constants.WINK_COUNTER > self.constants.WINK_CONSECUTIVE_FRAMES:
                        self.constants.WINK_COUNTER = 0
                        pag.click(button='right')
                        os.system('say "Right"');

            elif leftEAR < rightEAR:
                if leftEAR < self.constants.EYE_AR_THRESH:
                    self.constants.WINK_COUNTER += 1


                    if self.constants.WINK_COUNTER > self.constants.WINK_CONSECUTIVE_FRAMES:
                        self.constants.WINK_COUNTER = 0
                        pag.click(button='left')
                        os.system('say "Left"')

            else:
                self.constants.WINK_COUNTER = 0


    def detectBlink(self, leftEye, rightEye):
        leftEAR = self.measureUtils.eye_aspect_ratio(leftEye)
        rightEAR = self.measureUtils.eye_aspect_ratio(rightEye)
        rightCosin = self.measureUtils.measureCosin(rightEye)
        leftCosin = self.measureUtils.measureCosin(leftEye)
        self.EAR = (leftEAR + rightEAR) / 2.0
        self.diff_ear = np.abs(leftEAR - rightEAR)
        self.diff_cos = abs(leftCosin - rightCosin)

        #if self.diff_ear > self.constants.WINK_AR_DIFF_THRESH:
        if self.diff_cos < 0.22:
            print("Cosinus diff", self.diff_cos)
            if leftEAR > rightEAR:
                if rightCosin >= 0.82 and leftCosin < 0.82:
                    self.constants.WINK_COUNTER += 1

                    if self.constants.WINK_COUNTER > self.constants.WINK_CONSECUTIVE_FRAMES:
                        pag.click(button='right')
                        os.system('say "Right"');
                        self.constants.WINK_COUNTER = 0


            elif leftEAR < rightEAR:
                if leftCosin >= 0.82 and rightCosin < 0.82:
                    self.constants.WINK_COUNTER += 1
                    #print("Cosin left", leftCosin)

                    if self.constants.WINK_COUNTER > self.constants.WINK_CONSECUTIVE_FRAMES:
                        pag.click(button='left')
                        os.system('say "Left"')
                        self.constants.WINK_COUNTER = 0

            else:
                self.constants.WINK_COUNTER = 0



    def detectBlinkCos(self, leftEye, rightEye):
        leftEAR = self.measureUtils.eye_aspect_ratio(leftEye)
        rightEAR = self.measureUtils.eye_aspect_ratio(rightEye)
        rightCosin = self.measureUtils.measureCosin(rightEye)
        leftCosin = self.measureUtils.measureCosin(leftEye)
        self.EAR = (leftEAR + rightEAR) / 2.0
        self.diff_ear = np.abs(leftEAR - rightEAR)
        self.diff_cos = abs(leftCosin - rightCosin)

#        print("Normal right cosinus", rightCosin)
#        print("Normal left cosinus", rightCosin)

#        print("Both Blinking", self.diff_cos)
#        if self.diff_cos < 0.01:
#            self.constants.WINK_COUNTER = 0

        if self.diff_ear > self.constants.WINK_AR_DIFF_THRESH:
#            if leftCosin >= 0.82 and rightCosin >= 0.82:
#                #both eyes are closed
#                self.constants.WINK_COUNTER = 0

            if leftCosin < rightCosin:
                if rightCosin >= 0.82:
#                    print("Cosin right", rightCosin)
#                    print("Left right", leftCosin)
                    self.constants.WINK_COUNTER += 1
#                if rightEAR < self.constants.EYE_AR_THRESH:
#                    print("Cosin right", rightCosin)
#                    self.constants.WINK_COUNTER += 1


                    if self.constants.WINK_COUNTER > self.constants.WINK_CONSECUTIVE_FRAMES:
                        self.constants.WINK_COUNTER = 0
                        pag.click(button='right')
                        os.system('say "Right"');

            elif rightCosin < leftCosin:
                if leftCosin >= 0.82:
                    #print("Left right", leftCosin)
                #if leftEAR < self.constants.EYE_AR_THRESH:
                    self.constants.WINK_COUNTER += 1
                    if self.constants.WINK_COUNTER > self.constants.WINK_CONSECUTIVE_FRAMES:
                        self.constants.WINK_COUNTER = 0
                        pag.click(button='left')
                        os.system('say "Left"')

            else:
                self.constants.WINK_COUNTER = 0

    def detectScroll(self, scroll_mode, mouth):
        mar = self.measureUtils.mouth_aspect_ratio(mouth)
        if mar > self.constants.MOUTH_AR_THRESH:
            self.constants.MOUTH_COUNTER += 1

            if self.constants.MOUTH_COUNTER >= self.constants.MOUTH_AR_CONSECUTIVE_FRAMES:
                # if the alarm is not on, turn it on
                scroll_mode = not scroll_mode
                if scroll_mode:
                    os.system('say "Scroll on"')
                else:
                    os.system('say "Scroll off"')
                # SCROLL_MODE = not SCROLL_MODE
                self.constants.MOUTH_COUNTER = 0

        else:
            self.constants.MOUTH_COUNTER = 0

        return scroll_mode
