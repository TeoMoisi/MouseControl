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
        self._measureUtils = MeasureUtils()
        self._constants = Constants()

    def detectBlinkEAR(self, leftEye, rightEye):
        leftEAR = self._measureUtils.eye_aspect_ratio(leftEye)
        rightEAR = self._measureUtils.eye_aspect_ratio(rightEye)
        diff_ear = np.abs(leftEAR - rightEAR)

        if diff_ear > self._constants.WINK_AR_DIFF_THRESH:
            if rightEAR < leftEAR:
                if rightEAR < self._constants.EYE_AR_THRESH:
                    self._constants.WINK_COUNTER += 1

                    if self._constants.WINK_COUNTER > self._constants.WINK_CONSECUTIVE_FRAMES:
                        self._constants.WINK_COUNTER = 0
                        pag.click(button='right')
                        os.system('say "Right"');

            elif leftEAR < rightEAR:
                if leftEAR < self._constants.EYE_AR_THRESH:
                    self._constants.WINK_COUNTER += 1

                    if self._constants.WINK_COUNTER > self._constants.WINK_CONSECUTIVE_FRAMES:
                        self._constants.WINK_COUNTER = 0
                        pag.click(button='left')
                        os.system('say "Left"')

            else:
                self._constants.WINK_COUNTER = 0


    def detectBlinkCos(self, leftEye, rightEye):
        rightCosin = self._measureUtils.measure_cosine(rightEye)
        leftCosin = self._measureUtils.measure_cosine(leftEye)
        self.diff_cos = abs(leftCosin - rightCosin)

        if self.diff_cos < self._constants.WINK_COS_DIFF_THRESH:
            print("Cosinus diff", self.diff_cos)
            if rightCosin > leftCosin:
                if rightCosin >= self._constants.COS_AR_THRESH and leftCosin < self._constants.COS_AR_THRESH :
                    self._constants.WINK_COUNTER += 1

                    if self._constants.WINK_COUNTER > self._constants.WINK_CONSECUTIVE_FRAMES:
                        pag.click(button='right')
                        os.system('say "Right"');
                        self._constants.WINK_COUNTER = 0

            elif rightCosin < leftCosin:
                if leftCosin >= self._constants.COS_AR_THRESH  and rightCosin < self._constants.COS_AR_THRESH :
                    self._constants.WINK_COUNTER += 1

                    if self._constants.WINK_COUNTER > self._constants.WINK_CONSECUTIVE_FRAMES:
                        pag.click(button='left')
                        os.system('say "Left"')
                        self._constants.WINK_COUNTER = 0

            else:
                self._constants.WINK_COUNTER = 0


    def detectScroll(self, scroll_mode, mouth):
        mar = self._measureUtils.mouth_aspect_ratio(mouth)
        if mar > self._constants.MOUTH_AR_THRESH:
            self._constants.MOUTH_COUNTER += 1

            if self._constants.MOUTH_COUNTER >= self._constants.MOUTH_AR_CONSECUTIVE_FRAMES:
                scroll_mode = not scroll_mode
                if scroll_mode:
                    os.system('say "Scroll on"')
                else:
                    os.system('say "Scroll off"')
                self._constants.MOUTH_COUNTER = 0

        else:
            self._constants.MOUTH_COUNTER = 0

        return scroll_mode
