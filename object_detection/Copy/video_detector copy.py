import cv2
import cv2, imutils
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt6.QtGui import *
from PyQt6 import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QGradient, QIcon, QMovie,
                           QImage, QKeySequence, QLinearGradient, QPainter, QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QGridLayout, QLabel,
                               QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout, QWidget, QFileDialog)

import numpy as np
from PIL import Image as im
import time

np.random.seed(20)
class Video_Detector_obj:
    def __init__(self, videoPath, configPath, modelPath, classesPath):
        self.videoPath = videoPath
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        self.readClasses()
        
        #self.load_video = QLabel()
        #self.load_video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.Worker1 = Worker1()
        #self.Worker1.ImageUpdate.connect(self.ImageUpdatesSlot)

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()
        
        self.classesList.insert(0, '__Background__')

        self.colorList = np.random.uniform(low=0, high=255, size=(len(self.classesList), 3))
        
        print(self.classesList)

    def ImageUpdatesSlot(self, Image):
        self.load_video.setPixmap(QPixmap.fromImage(Image))


    def CancelFeed(self):
        self.Worker1.stop()

    def key_run():
        global key
        print("Run func")
        key = True

    def key_stop():
        global key
        print("Stop func")
        key = False


    def onVideo(self, grid_video_detect, video_screenshot_btn, video_play_btn, video_stop_btn):
        global image
        cap = cv2.VideoCapture(self.videoPath)
        temp_path = self.videoPath

        if (cap.isOpened()==False):
            print("Error opening file...")
            return

        (success, image) = cap.read()

        startTime = 0

        while success:
            currentTime = time.time()
            fps = 1/(currentTime - startTime)
            startTime = currentTime
            classLabelIDs, confidences, bboxs =  self.net.detect(image, confThreshold = 0.5)

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

                        cv2.rectangle(image, (x,y), (x+w, y+h), color=classColor, thickness=1)
                        cv2.putText(image, displayText, (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)

            cv2.putText(image, "FPS: " + str(int(fps)), (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            #cv2.imshow("Result", image)


            
            load_video = QLabel()
            image = imutils.resize(image, width = 1500)
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            load_video.setPixmap(QPixmap.fromImage(image))
            load_video.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid_video_detect.addWidget(load_video, 0, 1)




            #self.Worker1.start()
            #grid_video_detect.addWidget(self.load_video, 0, 1)

            
            global key
            key = cv2.waitKey(1) & 0xFF
            #if key == ord("q"):
            #    break
            if key == False:
                print("Break")
                break

            if temp_path != self.videoPath:
                print("Changed!!!")
                temp_path = self.videoPath
                break

            (success, image) = cap.read()
        cv2.destroyAllWindows()


#class Worker1(QThread):
#    ImageUpdate = pyqtSignal(QImage)
#    def run(self):
#        self.TreadActive = True
#        Capture = cv2.VideoCapture("C:\\Users\\Max\\Downloads\\videos\\Running - 294.mp4")
#        while self.TreadActive:
#            ret, frame = Capture.read()
#            if ret:
#                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                #FlippedImage = cv2.flip(Image, 1)
#                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
#                Pic = ConvertToQtFormat.scaled(1500, 3000, Qt.KeepAspectRatio)
#                self.ImageUpdate.emit(Pic)
#    def stop(self):
#        self.TreadActive = False
#        self.quit()
