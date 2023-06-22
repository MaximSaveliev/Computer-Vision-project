import cv2
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt6.QtGui import QPixmap, QImage
from PyQt6 import QtGui, QtCore, sip
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
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
class Image_Detector_obj: 
    def __init__(self, imagePath, configPath, modelPath, classesPath):
        self.imagePath = imagePath
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(700, 700)
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

    def onImage(self, grid_image_detect):
        global image
        image = cv2.imread(self.imagePath)
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        
        classLabelIDs, confidences, bboxs =  self.net.detect(image, confThreshold = 0.5)

        bboxs = list(bboxs)
        confidences = list(np.array(confidences).reshape(1,-1)[0])
        confidences = list(map(float, confidences))

        bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold = 0.3, nms_threshold = 0.2)

        if len(bboxIdx) != 0:
                    for i in range(0, len(bboxIdx)):

                        bbox = bboxs[np.squeeze(bboxIdx[i])]
                        classConfidence = confidences[np.squeeze(bboxIdx[i])]
                        classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                        classLabel = self.classesList[classLabelID]
                        classColor = [int(c) for c in self.colorList[classLabelID]]

                        displayText = "{}:{:.2f}".format(classLabel, classConfidence)

                        x,y,w,h = bbox

                        cv2.rectangle(image, (x,y), (x+w, y+h), color=classColor, thickness = 1)
                        cv2.putText(image, displayText, (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)
     
        q_image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        load_image = QLabel()
        detected_image = QPixmap(q_image)
        load_image.setPixmap(detected_image.scaled(800, 500, Qt.AspectRatioMode.KeepAspectRatio))
        load_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_image_detect.addWidget(load_image, 0, 2)

        #cv2.imshow('img', image)
        cv2.waitKey()

    def saveImage():
        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;GIF(*.gif);;BMP(*.bmp)")[0]
        cv2.imwrite(filename, image)
