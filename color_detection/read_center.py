import cv2 as cv
from scipy.spatial import KDTree
import webcolors
from functools import partial
import cv2, imutils, os, sys
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt6.QtGui import *
from PyQt6 import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, Signal, Slot, QThread, QThreadPool)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QGradient, QIcon, QMovie, QAction,
                           QImage, QKeySequence, QLinearGradient, QPainter, QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QGridLayout, QLabel,
                               QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout, QWidget, QFileDialog)

import numpy as np
from PIL import Image as im
import time

class Camera_color_detect_label(QWidget):
    def __init__(self, grid_camera_detect, camera_play_btn, camera_stop_btn, camera_screenshot_btn):
        super().__init__()
        self.screenshot = 'Snapshot ' + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png'
        self.temp_image = None

        self.load_video = QLabel()

        self.th = Thread()
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)

        grid_camera_detect.addWidget(self.load_video, 0, 1)

        self.start(camera_play_btn, camera_stop_btn, grid_camera_detect)
        camera_play_btn.clicked.connect(partial(self.start, camera_play_btn, camera_stop_btn, grid_camera_detect))
        camera_stop_btn.clicked.connect(partial(self.kill_thread, camera_play_btn, camera_stop_btn))
        camera_screenshot_btn.clicked.connect(self.make_screenshot)
        camera_play_btn.setEnabled(True)
    

    @Slot()
    def make_screenshot(self):
        self.th.screenshot_img()

    @Slot()
    def kill_thread(self, camera_play_btn, camera_stop_btn):
        print("Finishing...")
        camera_play_btn.setEnabled(True)
        camera_stop_btn.setEnabled(False)
        self.th.cap.release()
        cv2.destroyAllWindows()
        self.status = False
        self.th.terminate()
        self.th.exit()
        time.sleep(1)

    @Slot()
    def start(self, camera_play_btn, camera_stop_btn, grid_camera_detect):
        grid_camera_detect.addWidget(self.load_video, 0, 1)
        print("Starting...")
        camera_play_btn.setEnabled(False)
        camera_stop_btn.setEnabled(True)
        self.th.start()

    @Slot(QImage)
    def setImage(self, image):
        self.load_video.setPixmap(QPixmap.fromImage(image))
        self.load_video.setAlignment(Qt.AlignmentFlag.AlignCenter)



class Thread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.status = True
        self.cap = True

    def convert_rgb_to_names(rgb_tuple):
        
        # a dictionary of all the hex and their respective names in css3
        css3_db = webcolors.CSS3_HEX_TO_NAMES
        names = []
        rgb_values = []
        for color_hex, color_name in css3_db.items():
            names.append(color_name)
            rgb_values.append(webcolors.hex_to_rgb(color_hex))
        
        kdt_db = KDTree(rgb_values)
        distance, index = kdt_db.query(rgb_tuple)
        return f'{names[index]}'

    def screenshot_img(self):        
        self.screenshot = 'Snapshot ' + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png'
        cv.imwrite(self.screenshot, self.color_frame)


    def run(self):
        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

        if (self.cap.isOpened() == False):
            print("Error opening file...")
            return


        while self.status:
            _, frame = self.cap.read()
            frame = cv.flip(frame, 1)
            height, width, _ = frame.shape
            cx = int(width/2)
            cy = int(height/2)

            bgr_center = frame[cy, cx]
            color_name = Thread.convert_rgb_to_names((int(bgr_center[2]), int(bgr_center[1]), int(bgr_center[0])))

            text_size = cv.getTextSize(color_name, cv.FONT_HERSHEY_SIMPLEX, 1, 4)[0]
            text_width, text_height = text_size[0], text_size[1]
            text_x = int(width/2 - text_width/2)
            text_y = int(height/2 + text_height/2)
            cv.putText(frame, color_name, (text_x, 100), 0, 1, (0, 0, 0), 6)
            cv.putText(frame, color_name, (text_x, 100), 0, 1, (int(bgr_center[0]), int(bgr_center[1]), int(bgr_center[2])), 4)
            
            cv.circle(frame, (cx, cy), 10, (255,255,255), 3)

            #cv.imshow('Cat', frame)
            #key = cv.waitKey(1)

            #if key == 27:
            #    break

            self.color_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            self.color_frame = imutils.resize(frame, width = 1500)
            h, w, ch = self.color_frame.shape
            image = QImage(self.color_frame.data, w, h, ch * w, QImage.Format_RGB888).rgbSwapped()
            
            self.updateFrame.emit(image)

        self.cap.release()
        cv.destroyAllWindows()
        sys.exit(-1)