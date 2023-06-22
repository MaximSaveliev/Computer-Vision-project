from object_detection.image_detector import *
import os
import sys
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt6.QtGui import QPixmap
from PyQt6 import QtGui, QtCore, sip
from PyQt6.QtGui import QCursor
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QGradient, QIcon, QMovie,
                           QImage, QKeySequence, QLinearGradient, QPainter, QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QGridLayout, QLabel,
                               QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout, QWidget, QFileDialog)
                               
imagePath = ""

def main_image_obj(imagePath, grid_image_detect):
    rootDirectory = os.path.dirname(__file__)
    
    #imagePath = os.path.join(rootDirectory, "Images", "img10.jpg")
    configPath = os.path.join(rootDirectory, "data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join(rootDirectory, "data", "frozen_inference_graph.pb")
    classesPath = os.path.join(rootDirectory, "data", "coco.names")

    detector = Image_Detector_obj(imagePath[0], configPath, modelPath, classesPath)
    detector.onImage(grid_image_detect)

if __name__== '__main__':
    main_image_obj()