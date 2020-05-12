# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
import numpy as np

class MeasureUtils:
    def __init__(self):
        pass

    def eye_aspect_ratio(self, eye):
        firstDistance = np.linalg.norm(eye[1] - eye[5])
        secondDistance = np.linalg.norm(eye[2] - eye[4])

            # Compute the euclidean distance between the horizontal
            # eye landmark (x, y)-coordinates
        thirdDistance = np.linalg.norm(eye[0] - eye[3])

            # Compute the eye aspect ratio
        ear = (firstDistance + secondDistance) / (2.0 * thirdDistance)

            # Return the eye aspect ratio
        return ear

    def direction(self, nose_point, anchor_point, w, h, multiple=1):
        nx, ny = nose_point
        x, y = anchor_point

        if nx > x + multiple * w:
            return 'right'
        elif nx < x - multiple * w:
            return 'left'

        if ny > y + multiple * h:
            return 'down'
        elif ny < y - multiple * h:
            return 'up'

        return '-'

    def mouth_aspect_ratio(self, mouth):
        # Compute the euclidean distances between the three sets
        # of vertical mouth landmarks (x, y)-coordinates
        A = np.linalg.norm(mouth[13] - mouth[19])
        B = np.linalg.norm(mouth[14] - mouth[18])
        C = np.linalg.norm(mouth[15] - mouth[17])

        # Compute the euclidean distance between the horizontal
        # mouth landmarks (x, y)-coordinates
        D = np.linalg.norm(mouth[12] - mouth[16])

        # Compute the mouth aspect ratio
        mar = (A + B + C) / (2 * D)

        # Return the mouth aspect ratio
        return mar

    def distance(self, nose_point, anchor_point, w, h):
        nx, ny = nose_point
        x, y = anchor_point
        if (nx - x) >= 2 * w:
            return "swipe right"
        if (nx - x) <= -2 * w:
            return "swipe left"


