# face color analysis given eye center position

import string
import sys
import os
import numpy as np
import cv2, imutils
import argparse
import time
import colorsys
import math
from PIL import Image
from functools import partial
import time
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)
from collections import Counter


from mtcnn.mtcnn import MTCNN

detector = MTCNN()


def closest_eye_color(requested_color):
    min_distance = None
    closest_name = None
    for color_name, color_rgb in predefined_eye_colors.items():
        distance = math.sqrt(
            (color_rgb[0] - requested_color[0]) ** 2
            + (color_rgb[1] - requested_color[1]) ** 2
            + (color_rgb[2] - requested_color[2]) ** 2
        )
        if min_distance is None or distance < min_distance:
            min_distance = distance
            closest_name = color_name
    return closest_name


predefined_eye_colors = {
    "brown": (165, 42, 42),
    "blue": (30, 144, 255),
    "green": (50, 205, 50),
    "hazel": (191, 162, 45),
    "black": (0, 0, 0),
    "amber": (255, 191, 0),
}

class Thread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.trained_file = os.path.join(cv2.data.haarcascades, "haarcascade_eye.xml")
        self.status = True
        self.cap = True

    def set_video_file(self, videoPath):
        self.videoPath = videoPath    

    def screenshot_img(self):        
        self.screenshot = 'Snapshot ' + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png'
        cv2.imwrite(self.screenshot, self.color_frame)

    def run(self):
        self.cap = cv2.VideoCapture(self.videoPath)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        if (self.cap.isOpened() == False):
            print("Error opening file...")
            return

        while self.status:
            cascade = cv2.CascadeClassifier(self.trained_file)
            _, frame = self.cap.read()

            # Reading frame in gray scale to process the pattern
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            detections = cascade.detectMultiScale(
                gray_frame, scaleFactor=1.3, minNeighbors=10, minSize=(40, 40),
                maxSize = (100,100)
            )

            # Drawing green rectangle around the pattern
            for (x, y, w, h) in detections:
                pos_ori = (x, y)
                pos_end = (x + w, y + h)
                color = (23, 195, 178)

                cv2.rectangle(frame, pos_ori, pos_end, color, 2)

            # Reading the image in RGB to display it
            self.color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.color_frame = imutils.resize(frame, width = 1500)

            # Creating and scaling QImage
            h, w, ch = self.color_frame.shape
            img = QImage(self.color_frame.data, w, h, ch * w, QImage.Format_RGB888).rgbSwapped()

            # Emit signal
            self.updateFrame.emit(img)
        self.cap.release()
        cv2.destroyAllWindows()
        sys.exit(-1)

class Video_Detector_eyes(QWidget):
    def __init__(self, videoPath, grid_video_detect, video_play_btn, video_stop_btn, video_screenshot_btn):
        super().__init__()
        self.videoPath = videoPath[0]

        self.screenshot = 'Snapshot ' + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png'
        self.temp_image = None


        self.load_video = QLabel()

        self.th = Thread()
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)

        
        grid_video_detect.addWidget(self.load_video, 0, 1)

        self.start(video_play_btn, video_stop_btn, grid_video_detect)
        video_play_btn.clicked.connect(partial(self.start, video_play_btn, video_stop_btn, grid_video_detect))
        video_stop_btn.clicked.connect(partial(self.kill_thread, video_play_btn, video_stop_btn))
        video_screenshot_btn.clicked.connect(self.make_screenshot)
        video_stop_btn.setEnabled(True)


    @Slot()
    def make_screenshot(self):
        self.th.screenshot_img()

    @Slot()
    def kill_thread(self, video_play_btn, video_stop_btn):
        print("Finishing...")
        video_play_btn.setEnabled(True)
        video_stop_btn.setEnabled(False)
        self.th.cap.release()
        cv2.destroyAllWindows()
        self.status = False
        self.th.exit()
        time.sleep(1)

    @Slot()
    def start(self, video_play_btn, video_stop_btn, grid_video_detect):
        grid_video_detect.addWidget(self.load_video, 0, 1)
        print("Starting...")
        video_play_btn.setEnabled(False)
        video_stop_btn.setEnabled(True)
        self.th.set_video_file(self.videoPath)
        self.th.start()

    @Slot(QImage)
    def setImage(self, image):
        self.load_video.setPixmap(QPixmap.fromImage(image))
        self.load_video.setAlignment(Qt.AlignmentFlag.AlignCenter)
