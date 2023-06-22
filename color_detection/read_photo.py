import cv2 as cv
import os
from scipy.spatial import KDTree
import webcolors
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPixmap
from PyQt6 import QtGui, QtCore, sip
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QCursor
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QGradient, QIcon, QMovie,
                           QImage, QKeySequence, QLinearGradient, QPainter, QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QGridLayout, QLabel,
                               QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout, QWidget, QFileDialog)

clicked_color = None
frame = None
frameCopy = None
image_path = ""

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


def color_detecting(event, x, y, flags, param):
    global clicked_color
    global frame

    if event == cv.EVENT_LBUTTONDOWN:
        clicked_color = frame[y, x]


def main_image_color(image_path, grid_image_detect):
    global frame
    rootDirectory = os.path.dirname(__file__)
    #image_path = os.path.join(rootDirectory, "Media", "photo5.jpg")
    frame = cv.imread(image_path)
    height, width, _ = frame.shape
    bytesPerLine = 3 * width

    # Create a QLabel to display the image
    load_image = QLabel()
    load_image.setAlignment(Qt.AlignCenter)
    grid_image_detect.addWidget(load_image, 0, 2)

    # Connect the mousePressEvent function to the mousePressEvent signal
    load_image.installEventFilter(load_image)
    load_image.setMouseTracking(True)

    def eventFilter(source, event):
        if event.type() == QEvent.Type.MouseButtonPress and source is load_image:
            return mouseMoveEvent(event)
        return QLabel.eventFilter(load_image, source, event)

    load_image.eventFilter = eventFilter

    def mouseMoveEvent(event):
        global clicked_color
        pos = event.pos()
        # Get the color of the pixel at the cursor position
        x = int(pos.x() * width / 800)
        y = int(pos.y() * height / 500)
        if event.type() == QEvent.Type.MouseButtonPress:
            clicked_color = frame[y, x]
        print("Color at pixel", x, y, ":", clicked_color)
        return QLabel.mouseMoveEvent(load_image, event)

    load_image.mouseMoveEvent = mouseMoveEvent


    while True:
        global frameCopy
        # Redraw the entire image with the new text
        frameCopy = frame.copy()
        if clicked_color is not None:
            color_name = convert_rgb_to_names((int(clicked_color[2]), int(clicked_color[1]), int(clicked_color[0])))

            text_size = cv.getTextSize(color_name, cv.FONT_HERSHEY_SIMPLEX, 2, 5)[0]
            # Draw a rectangle behind the text
            text_width, text_height = text_size[0], text_size[1]
            text_x = int(width/2 - text_width/2)
            text_y = int(height/2 + text_height/2)
            cv.rectangle(frameCopy, (text_x - 10, 115), (text_x + text_width + 7, 10 + text_height - 5), (255, 255, 255), -1)
            cv.putText(frameCopy, color_name, (text_x, 100), 0, 2, (0, 0, 0), 7)
            cv.putText(frameCopy, color_name, (text_x, 100), 0, 2, (int(clicked_color[0]), int(clicked_color[1]), int(clicked_color[2])), 5)

        
        q_image = QImage(frameCopy, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        detected_image = QPixmap.fromImage(q_image)
        load_image.setPixmap((detected_image.scaled(800, 500, Qt.AspectRatioMode.KeepAspectRatio)))
        load_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_image_detect.addWidget(load_image, 0, 2)

        cv.imshow('Project', frameCopy)
        cv.namedWindow("Project")
        cv.setMouseCallback('Project', color_detecting)
        key = cv.waitKey(1)
        if key == 27:
            break
    cv.destroyAllWindows()

def saveImage_color():
    filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;GIF(*.gif);;BMP(*.bmp)")[0]
    cv.imwrite(filename, frameCopy)