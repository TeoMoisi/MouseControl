# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
import numpy as np

class MeasureUtils:
    def __init__(self):
        pass

    def eye_aspect_ratio(self, eye):
        firstDistance = np.linalg.norm(eye[1] - eye[5])
        secondDistance = np.linalg.norm(eye[2] - eye[4])
        thirdDistance = np.linalg.norm(eye[0] - eye[3])

        ear = (firstDistance + secondDistance) / (2.0 * thirdDistance)
        return ear

    def measure_cosine(self, eye):
        a = np.linalg.norm(eye[2] - eye[4])
        b = np.linalg.norm(eye[3] - eye[4])
        c = np.linalg.norm(eye[2] - eye[3])

        cosinA = (c*c + b*b - a*a) / (2 * c * b)
        return cosinA


    def direction(self, nose_point, anchor_point, w, h):
        nx, ny = nose_point
        x, y = anchor_point
        multiple = 1

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
        A = np.linalg.norm(mouth[13] - mouth[19])
        B = np.linalg.norm(mouth[14] - mouth[18])
        C = np.linalg.norm(mouth[15] - mouth[17])
        D = np.linalg.norm(mouth[12] - mouth[16])

        mar = (A + B + C) / (2 * D)
        return mar

    def distance(self, nose_point, anchor_point, w, h):
        nx, ny = nose_point
        x, y = anchor_point
        if (nx - x) >= 2 * w:
            return "swipe right"
        if (nx - x) <= -2 * w:
            return "swipe left"


