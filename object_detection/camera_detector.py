import cv2
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

np.random.seed(20)
class Camera_Detector_obj(QWidget): 
    def __init__(self, configPath, modelPath, classesPath, grid_camera_detect, camera_play_btn, camera_stop_btn, camera_screenshot_btn):
        super().__init__()
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath
        self.camera_play_btn = camera_play_btn
        self.camera_stop_btn = camera_stop_btn

        self.screenshot = 'Snapshot ' + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png'
        self.temp_image = None


        self.load_video = QLabel()

        self.th = Thread()
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)

        
        grid_camera_detect.addWidget(self.load_video, 0, 1)

        self.start(camera_play_btn, camera_stop_btn, grid_camera_detect)
        camera_play_btn.clicked.connect(partial(self.start, camera_play_btn, camera_stop_btn, grid_camera_detect))
        camera_stop_btn.clicked.connect(self.kill_thread)
        camera_screenshot_btn.clicked.connect(self.make_screenshot)
        camera_play_btn.setEnabled(True)

    @Slot()
    def make_screenshot(self):
        self.th.screenshot_img()

    @Slot()
    def set_models(self, configPath, modelPath, classesPath):
        self.th.set_files(configPath, modelPath, classesPath)

    @Slot()
    def kill_thread(self):
        print("Finishing...")
        self.camera_play_btn.setEnabled(True)
        self.camera_stop_btn.setEnabled(False)
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
        self.th.set_files(self.configPath, self.modelPath, self.classesPath)
        self.th.start()

    @Slot(QImage)
    def setImage(self, image):
        self.load_video.setPixmap(QPixmap.fromImage(image))
        self.load_video.setAlignment(Qt.AlignmentFlag.AlignCenter)





class Thread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        #self.trained_file = None
        self.status = True
        self.cap = True
        self.configPath = None
        self.modelPath = None
        self.classesPath = None



    def set_files(self, configPath, modelPath, classesPath):
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        self.readClasses()

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()
        
        self.classesList.insert(0, '__Background__')

        self.colorList = np.random.uniform(low=0, high=255, size=(len(self.classesList), 3))
        
        print(self.classesList)

    def screenshot_img(self):        
        self.screenshot = 'Snapshot ' + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png'
        cv2.imwrite(self.screenshot, self.color_frame)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))
        self.cap.set(3, 1920)
        self.cap.set(4, 1080)
        if (self.cap.isOpened()==False):
            print("Error opening file...")
            return

        startTime = 0
        while self.status:
            ret, frame = self.cap.read()
            if not ret:
                continue

            currentTime = time.time()
            fps = 1/(currentTime - startTime)
            startTime = currentTime
            classLabelIDs, confidences, bboxs =  self.net.detect(frame, confThreshold = 0.5)

            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1,-1)[0])
            confidences = list(map(float, confidences))

            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold = 0.5, nms_threshold = 0.2)

            if len(bboxIdx) != 0:
                    for i in range(0, len(bboxIdx)):

                        bbox = bboxs[np.squeeze(bboxIdx[i])]
                        classConfidence = confidences[np.squeeze(bboxIdx[i])]
                        classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                        classLabel = self.classesList[classLabelID]
                        classColor = [int(c) for c in self.colorList[classLabelID]]

                        displayText = "{}:{:.2f}".format(classLabel, classConfidence)

                        x,y,w,h = bbox

                        cv2.rectangle(frame, (x,y), (x+w, y+h), color=classColor, thickness=1)
                        cv2.putText(frame, displayText, (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

            cv2.putText(frame, "FPS: " + str(int(fps)), (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            #cv2.imshow("Result", image)

            self.color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            
            self.color_frame = imutils.resize(frame, width = 1500)
            h, w, ch = self.color_frame.shape
            image = QImage(self.color_frame.data, w, h, ch * w, QImage.Format_RGB888).rgbSwapped()

            self.updateFrame.emit(image)
        cv2.destroyAllWindows()
        sys.exit(-1)
