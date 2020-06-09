# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
from imutils import face_utils

class Constants:
    def __init__(self):
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        (nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]
        (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
        self.lStart = lStart
        self.lEnd = lEnd
        self.rStart = rStart
        self.rEnd = rEnd
        self.nStart = nStart
        self.nEnd = nEnd
        self.mStart = mStart
        self.mEnd = mEnd

        # colours
        self.WHITE_COLOR = (255, 255, 255)
        self.YELLOW_COLOR = (0, 255, 255)
        self.RED_COLOR = (0, 0, 255)
        self.GREEN_COLOR = (0, 255, 0)
        self.BLUE_COLOR = (255, 0, 0)
        self.BLACK_COLOR = (0, 0, 0)

        # camera dimensions
        self.CAM_W = 640
        self.CAM_H = 480

        # ar
        self.EYE_AR_THRESH = 0.19
        self.EYE_AR_CONSECUTIVE_FRAMES = 10
        self.WINK_AR_DIFF_THRESH = 0.00
        self.WINK_AR_CLOSE_THRESH = 0.19
        self.WINK_CONSECUTIVE_FRAMES = 3
        self.WINK_COUNTER = 0
        self.SCROLL_MODE = False
        self.EYE_COUNTER = 0

        # rectangle Constants
        self.WIDTH = 50
        self.HEIGHT = 35
        self.ANCHOR_POINT = (int(self.CAM_W / 2), int(self.CAM_H / 2))

        # cursor settings
        self.DRAG_MOTION = 20

        # mouth
        self.MOUTH_AR_THRESH = 0.25
        self.MOUTH_AR_CONSECUTIVE_FRAMES = 15
        self.MOUTH_COUNTER = 0
