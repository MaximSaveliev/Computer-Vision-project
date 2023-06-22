# face color analysis given eye center position

import string
import sys
import os
import numpy as np
import cv2
import argparse
import time
import colorsys
import math
from PIL import Image
import webcolors
from collections import Counter
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


from mtcnn.mtcnn import MTCNN

detector = MTCNN()


imagePath = ""
image = None

def closest_eye_color(requested_color):
    min_distance = None
    closest_name = None
    for color_name, color_rgb in predefined_eye_colors.items():
        distance = math.sqrt(
            (color_rgb[0] - requested_color[0]) ** 2 +
            (color_rgb[1] - requested_color[1]) ** 2 +
            (color_rgb[2] - requested_color[2]) ** 2
        )
        if min_distance is None or distance < min_distance:
            min_distance = distance
            closest_name = color_name
    return closest_name

predefined_eye_colors = {
    "brown": (165, 42, 42),
    "blue": (30, 144, 255),
    "green": (50, 205, 50),
    "ocean green": (50, 109, 113),
    "grey blue": (105,103,95),
    "hazel": (191, 162, 45),
    "black": (0, 0, 0),
    "amber": (255, 191, 0)
}



def eyeColorByImage(path, grid_image_detect):
    global image
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    height, width, _ = image.shape
    #new_width = 500
    #aspect_ration = float(height / width)
    #new_height = int(new_width * aspect_ration)
    #image = cv2.resize(image, (new_width, new_height), interpolation = cv2.INTER_LINEAR)
    bytesPerLine = 3 * width
    imgMask = np.zeros((image.shape[0], image.shape[1], 1))
    
    result = detector.detect_faces(image)
    if result == []:
        print('Warning: Can not detect any face in the input image!')
        return

    bounding_box = result[0]['box']
    left_eye = result[0]['keypoints']['left_eye']
    right_eye = result[0]['keypoints']['right_eye']

    radius = int((right_eye[0] - left_eye[0])/10)#aproximate eye radius  

    cv2.circle(imgMask, left_eye, int(radius), (255,255,255), -1)
    cv2.circle(imgMask, right_eye, int(radius), (255,255,255), -1)

    cv2.rectangle(image,
              (bounding_box[0], bounding_box[1]),
              (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
              (255,155,255),
              3)

    cv2.circle(image, left_eye, int(radius), (0, 155, 255), 3)
    cv2.circle(image, right_eye, int(radius), (0, 155, 255), 3)


    im = Image.open(path)
    pixels = im.load()
    for x in range(left_eye[0] - radius, left_eye[0] + radius):
        for y in range(left_eye[1] - radius, left_eye[1] + radius):
        # Check if the pixel is within the circle using the distance formula
            if ((x - left_eye[0]) ** 2 + (y - left_eye[1]) ** 2) ** 0.5 <= radius:
            # Get the color of the pixel
                color = pixels[x, y]

    
    main_color = closest_eye_color(color)
    
    print("\n\nDominant Eye Color: ", main_color)
    
    
    label = 'Dominant Eye Color: %s' % main_color
    text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 3, 5)[0]
    # Draw a rectangle behind the text
    text_width, text_height = text_size[0], text_size[1]
    text_x = int(width/2 - text_width/2)
    text_y = int(height/2 + text_height/2)
    cv2.putText(image, label, (text_x, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (155,255,0), 5)


    q_image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
    load_image = QLabel()
    detected_image = QPixmap(q_image)
    load_image.setPixmap(detected_image.scaled(1000, 700, Qt.AspectRatioMode.KeepAspectRatio))
    load_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
    grid_image_detect.addWidget(load_image, 0, 2)



    #cv2.imshow('EYE-COLOR-DETECTION', image)

def eyeColorByVideo(image):
    imgMask = np.zeros((image.shape[0], image.shape[1], 1))
    
    result = detector.detect_faces(image)
    if result == []:
        print('Warning: Can not detect any face in the input image!')
        return

    bounding_box = result[0]['box']
    left_eye = result[0]['keypoints']['left_eye']
    right_eye = result[0]['keypoints']['right_eye']

    radius = int((right_eye[0] - left_eye[0])/10)#aproximate eye radius  

    cv2.circle(imgMask, left_eye, int(radius), (255,255,255), -1)
    cv2.circle(imgMask, right_eye, int(radius), (255,255,255), -1)

    cv2.rectangle(image,
              (bounding_box[0], bounding_box[1]),
              (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
              (255,155,255),
              2)

    cv2.circle(image, left_eye, int(radius), (0, 155, 255), 1)
    cv2.circle(image, right_eye, int(radius), (0, 155, 255), 1)
    
    #im = Image.open(path)
    #pixels = im.load()
    for x in range(left_eye[0] - radius, left_eye[0] + radius):
        for y in range(left_eye[1] - radius, left_eye[1] + radius):
        # Check if the pixel is within the circle using the distance formula
            if ((x - left_eye[0]) ** 2 + (y - left_eye[1]) ** 2) ** 0.5 <= radius:
            # Get the color of the pixel
                color = image[x, y]

    
    main_color = closest_eye_color(color)
    
    print("\n\nDominant Eye Color: ", main_color)
    
    
    label = 'Dominant Eye Color: %s' % main_color  
    cv2.putText(image, label, (left_eye[0]-10, left_eye[1]-40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (155,255,0))
    #cv2.imshow('EYE-COLOR-DETECTION', image)

def main_image_eye(imagePath, grid_image_detect):
    path = imagePath       
    #send imagepath image 
    eyeColorByImage(path, grid_image_detect)
    cv2.waitKey(0)
    
    # video or webcam send frame
    #cap = cv2.VideoCapture(0)
    #while True:
    #    ret, frame = cap.read()
    #    eyeColorByVideo(frame)
    #    cv2.imshow("123",frame)
    #    
    #    if cv2.waitKey(1) & 0xFF == ord('q'):
    #        break
    #cap.release()
    cv2.destroyAllWindows()

def saveImage_eye():
        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;GIF(*.gif);;BMP(*.bmp)")[0]
        cv2.imwrite(filename, image)