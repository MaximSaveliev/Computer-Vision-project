import sys
import ctypes
from object_detection.image import *
from object_detection.image_detector import *
from object_detection.video import *
from object_detection.video_detector import *
from object_detection.camera import *
from object_detection.camera_detector import *
from color_detection.read_photo import *
from color_detection.read_center import *
from color_detection.read_mouse_click import *
from eye_detection.EyeDetector2 import *
from eye_detection.EyeDetector2_video import *
from eye_detection.EyeDetector2_camera import *
from functools import partial
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



grid = QGridLayout()
image_file = ""
video_file = ""

widgets = {
    "logo_robot": [],
    "robot_widget": [],
    "projectTitle": [],
    "startButton": [],
    "start_bnt_widget": [],
    "quitButton": [],
    "quit_bnt_widget": [],
    "backButton": [],
    "back_widget": [],
    "image_grid": [],
    "image1": [],
    "image2": [],
    "image3": [],
    "title1": [],
    "title2": [],
    "title3": [],
    "button1": [],
    "button2": [],
    "button3": [],
    "type_detection_widget": [],
    "image_detect": [],
    "image_detect_btn": [],
    "video_detect_btn": [],
    "webcam_detect_btn": [],
    "image_toolbar_widget": [],
    "image_detect": [],
    "image_import_btn": [],
    "image_download_btn": [],
    "video_toolbar_widget": [],
    "video_detect": [],
    "video_import_btn": [],
    "video_screenshot_btn": [],
    "video_play_btn": [],
    "video_stop_btn": [],
    "camera_detect": [],
    "camera_toolbar_widget": [],
    "camera_screenshot_btn": [],
    "camera_play_btn": [],
    "camera_stop_btn": []
}

def font():
    font = QFontDatabase.addApplicationFont("Fonts\Roboto-Regular.ttf")
    family = QFontDatabase.applicationFontFamilies(font)
    return family[0]


def reset_row_stretch():
    for i in range(0, grid.rowCount()):
        grid.setRowStretch(i, 0)


def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()






def display_image_eyes(grid_image_detect, image_detect_btn, image_download_btn):
    
    global image_file
    load_image = QLabel()
    image_file = ""
    image_file = QFileDialog.getOpenFileName(load_image, 'Open file', 'eye_detection\Images', "Image Files (*.jpg *.gif *.bmp *.png *.jpeg)")
    loaded_image = QPixmap(image_file[0])
    load_image.setPixmap(loaded_image.scaled(1000, 700, Qt.AspectRatioMode.KeepAspectRatio))
    load_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
    grid_image_detect.addWidget(load_image, 0, 1)
    image_detect_btn.clicked.connect(partial(main_image_eye, image_file[0], grid_image_detect),  Qt.ConnectionType.SingleShotConnection)
    #image_download_btn.clicked.connect(Detector.saveImage, Qt.ConnectionType.SingleShotConnection)
    return grid_image_detect


def display_video_eyes(grid_video_detect, video_detect_btn, video_play_btn, video_stop_btn, video_screenshot_btn):
    
    global video_file
    video_file = ""
    video_file = QFileDialog.getOpenFileName(None, 'Open file', 'eye_detection\Videos', "Video Files (*.mp4 *.mpeg *.avi)")
    video_detect_btn.clicked.connect(partial(Video_Detector_eyes, video_file, grid_video_detect, video_play_btn, video_stop_btn, video_screenshot_btn),  Qt.ConnectionType.SingleShotConnection)
    #image_download_btn.clicked.connect(Detector.saveImage, Qt.ConnectionType.SingleShotConnection)
    return grid_video_detect


def display_image_color(grid_image_detect, image_detect_btn, image_download_btn):
    
    global image_file
    load_image = QLabel()
    image_file = ""
    image_file = QFileDialog.getOpenFileName(load_image, 'Open file', 'color_detection\Images', "Image Files (*.jpg *.gif *.bmp *.png *.jpeg)")
    loaded_image = QPixmap(image_file[0])
    load_image.setPixmap(loaded_image.scaled(800, 500, Qt.AspectRatioMode.KeepAspectRatio))
    load_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
    grid_image_detect.addWidget(load_image, 0, 1)
    image_detect_btn.clicked.connect(partial(main_image_color, image_file[0], grid_image_detect),  Qt.ConnectionType.SingleShotConnection)
    #image_download_btn.clicked.connect(Detector.saveImage, Qt.ConnectionType.SingleShotConnection)
    return grid_image_detect


def display_image_obj(grid_image_detect, image_detect_btn, image_download_btn):
    
    global image_file
    load_image = QLabel()
    image_file = ""
    image_file = QFileDialog.getOpenFileName(load_image, 'Open file', 'object_detection\Images', "Image Files (*.jpg *.gif *.bmp *.png *.jpeg)")
    loaded_image = QPixmap(image_file[0])
    load_image.setPixmap(loaded_image.scaled(800, 500, Qt.AspectRatioMode.KeepAspectRatio))
    load_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
    grid_image_detect.addWidget(load_image, 0, 1)
    image_detect_btn.clicked.connect(partial(main_image_obj, image_file, grid_image_detect),  Qt.ConnectionType.SingleShotConnection)
    #image_download_btn.clicked.connect(Detector.saveImage, Qt.ConnectionType.SingleShotConnection)
    return grid_image_detect


def display_video_obj(grid_video_detect, video_detect_btn, video_play_btn, video_stop_btn, video_screenshot_btn):
    
    global video_file
    video_file = ""
    video_file = QFileDialog.getOpenFileName(None, 'Open file', 'object_detection\Videos', "Video Files (*.mp4 *.mpeg *.avi)")
    video_detect_btn.clicked.connect(partial(main_video_obj, video_file, grid_video_detect, video_play_btn, video_stop_btn, video_screenshot_btn),  Qt.ConnectionType.SingleShotConnection)
    #image_download_btn.clicked.connect(Detector.saveImage, Qt.ConnectionType.SingleShotConnection)
    return grid_video_detect



# Transition functions
def start_detection():
    reset_row_stretch()
    clear_widgets()
    frame2()


def goto_frame1():
    reset_row_stretch()
    clear_widgets()
    frame1()


def goto_frame2():
    reset_row_stretch()
    clear_widgets()
    frame2()


def goto_frame3():
    reset_row_stretch()
    clear_widgets()
    frame3()


def goto_image_eye_detect():
    reset_row_stretch()
    clear_widgets()
    image_eye_detect()


def goto_video_eye_detect():
    reset_row_stretch()
    clear_widgets()
    video_eye_detect()


def goto_camera_eye_detect():
    reset_row_stretch()
    clear_widgets()
    camera_eye_detect()


def goto_frame4():
    reset_row_stretch()
    clear_widgets()
    frame4()


def goto_image_color_detect():
    reset_row_stretch()
    clear_widgets()
    image_color_detect()


def goto_camera_color_detect_by_label():
    reset_row_stretch()
    clear_widgets()
    camera_color_detect_by_label()


def goto_camera_color_detect_by_click():
    reset_row_stretch()
    clear_widgets()
    camera_color_detect_by_click()


def goto_frame5():
    reset_row_stretch()
    clear_widgets()
    frame5()


def goto_image_obj_detect():
    reset_row_stretch()
    clear_widgets()
    image_obj_detect()


def goto_video_obj_detect():
    reset_row_stretch()
    clear_widgets()
    video_obj_detect()


def goto_camera_obj_detect():
    reset_row_stretch()
    clear_widgets()
    camera_obj_detect()



#*********************************************
#                  FRAME 1
#*********************************************
def frame1():
    window.setWindowTitle("APA Project")
    robot_horizontalLayout = QHBoxLayout()
    robot_widget = QWidget()
    start_horizontalLayout = QHBoxLayout()
    start_bnt_widget = QWidget()
    quit_horizontalLayout = QHBoxLayout()
    quit_bnt_widget = QWidget()

    # Append widgets to list widgets
    widgets["robot_widget"].append(robot_widget)
    widgets["start_bnt_widget"].append(start_bnt_widget)
    widgets["quit_bnt_widget"].append(quit_bnt_widget)

    # Display LOGO
    movie = QMovie(u"Photos/project_robot.gif")
    logo_robot = QLabel()
    logo_robot.setMovie(movie)
    logo_robot.setAlignment(Qt.AlignmentFlag.AlignCenter)
    logo_robot.setMaximumHeight(100)
    logo_robot.setScaledContents(True)
    logo_robot.setFixedSize(375, 250)
    movie.start()
    widgets["logo_robot"].append(logo_robot)

    # Display Project Title
    projectTitle = QLabel("Computer Vision Project 👨‍💻💻🖥️")
    projectTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
    projectTitle.setStyleSheet(
        "font-size: 50px;"
        "color: #14171A;"
        "margin: 50px 0 0 0;"
    )
    widgets["projectTitle"].append(projectTitle)

    # Start button widget
    startButton = QPushButton("START")
    startButton.setObjectName("startButton")
    startButton.setCursor(QCursor(Qt.PointingHandCursor))
    startButton.setStyleSheet(
        "#startButton{width: 300px;"
        "height: 50px;"
        "margin: 150px 0 0 0;"
        "padding: 5px 0;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 30px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#startButton:hover{background-color: '#1DA1F2';"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    startButton.setMaximumWidth(500)
    startButton.clicked.connect(start_detection)
    startButton.clicked.connect(movie.deleteLater)
    widgets["startButton"].append(startButton)

    # Quit button widget
    quitButton = QPushButton("QUIT")
    quitButton.setObjectName("quitButton")
    quitButton.setCursor(QCursor(Qt.PointingHandCursor))
    quitButton.setStyleSheet(
        "#quitButton{width: 300px;"
        "height: 50px;"
        "margin: 0 0 50px 0;"
        "padding: 5px 0;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#DD0031';"
        "border-radius: 30px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#quitButton:hover{background-color: '#DD0031';"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    quitButton.setMaximumWidth(500)
    widgets["quitButton"].append(quitButton)

    quitButton.clicked.connect(app.quit)

    # Vertical spacer
    verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    # Horizontal spacer
    horizontalSpacer = QSpacerItem(250, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    grid.addItem(verticalSpacer, 0, 0)
    robot_horizontalLayout.addItem(horizontalSpacer)
    robot_horizontalLayout.addWidget(widgets["logo_robot"][-1])
    robot_horizontalLayout.addItem(horizontalSpacer)
    robot_widget.setLayout(robot_horizontalLayout)
    grid.addWidget(widgets["robot_widget"][-1], 1, 0)
    grid.addItem(verticalSpacer, 2, 0)
    grid.addWidget(widgets["projectTitle"][-1], 3, 0)
    start_horizontalLayout.addItem(horizontalSpacer)
    start_horizontalLayout.addWidget(widgets["startButton"][-1])
    start_horizontalLayout.addItem(horizontalSpacer)
    start_bnt_widget.setLayout(start_horizontalLayout)
    grid.addWidget(widgets["start_bnt_widget"][-1], 4, 0)
    quit_horizontalLayout.addItem(horizontalSpacer)
    quit_horizontalLayout.addWidget(widgets["quitButton"][-1])
    quit_horizontalLayout.addItem(horizontalSpacer)
    quit_bnt_widget.setLayout(quit_horizontalLayout)
    grid.addWidget(widgets["quit_bnt_widget"][-1], 5, 0)
    grid.addItem(verticalSpacer, 6, 0)


#*********************************************
#                  FRAME 2
#*********************************************
def frame2():
    window.setWindowTitle("Detection Algorithms")
    back_horizontalLayout = QHBoxLayout()
    back_widget = QWidget()
    image_Layout = QGridLayout()
    image_grid = QWidget()

    # Append widgets to list widgets
    widgets["back_widget"].append(back_widget)
    widgets["image_grid"].append(image_grid)

    image1 = QLabel()
    image2 = QLabel()
    image3 = QLabel()
    title1 = QLabel("Eye Detection")
    title2 = QLabel("Color Detection")
    title3 = QLabel("Object Detection")

    
    widgets["image1"].append(image1)
    widgets["image2"].append(image2)
    widgets["image3"].append(image3)
    widgets["title1"].append(title1)
    widgets["title2"].append(title2)
    widgets["title3"].append(title3)

    image1.setObjectName("eye_detection")
    image2.setObjectName("color_detection")
    image3.setObjectName("object_detection")
    title1.setObjectName("title1")
    title2.setObjectName("title2")
    title3.setObjectName("title3")

    image1.setPixmap(QPixmap(u"Photos\eye_detection.png").scaled(425, 325, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation))
    image2.setPixmap(QPixmap(u"Photos\color_detection.png").scaled(425, 325, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation))
    image3.setPixmap(QPixmap(u"Photos\object_detection.png").scaled(425, 325, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation))

    image1.setScaledContents(True)
    image2.setScaledContents(True)
    image3.setScaledContents(True)

    image1.setAlignment(Qt.AlignmentFlag.AlignCenter)
    image2.setAlignment(Qt.AlignmentFlag.AlignCenter)
    image3.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title1.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title2.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title3.setAlignment(Qt.AlignmentFlag.AlignCenter)

    image1.setStyleSheet(
        "#eye_detection{"
        "border-image: url(Photos\color_detection.png) 0 0 0 0 stretch stretch;"
        "margin: 15px;}"
    )
    image2.setStyleSheet(
        "#color_detection{"
        "border-image: url(Photos\color_detection.png) 0 0 0 0 stretch stretch;"
        "margin: 15px;}"
    )
    image3.setStyleSheet(
        "#object_detection{"
        "border-image: url(Photos\object_detection.png) 0 0 0 0 stretch stretch;"
        "margin: 15px;}"
    )

    title1.setWordWrap(True)
    title2.setWordWrap(True)
    title3.setWordWrap(True)

    title1.setFont(QFont(font(), 24))
    title2.setFont(QFont(font(), 24))
    title3.setFont(QFont(font(), 24))

    title1.setStyleSheet(
        "#title1{"
        "font-style: italic;"
        "color: '#191414';"
        "margin: 15px;}"
    )
    title2.setStyleSheet(
        "#title2{"
        "font-style: italic;"
        "color: '#191414';"
        "margin: 15px;}"
    )
    title3.setStyleSheet(
        "#title3{"
        "font-style: italic;"
        "color: '#191414';"
        "margin: 15px;}"
    )

    button1 = QPushButton("Detect")
    button2 = QPushButton("Detect")
    button3 = QPushButton("Detect")

    widgets["button1"].append(button1)
    widgets["button2"].append(button2)
    widgets["button3"].append(button3)

    button1.setObjectName("eye_detection_btn")
    button2.setObjectName("color_detection_btn")
    button3.setObjectName("object_detection_btn")

    button1.setStyleSheet(
        "#eye_detection_btn{height: 42px;"
        "margin: 15px;"
        "padding: 5px 0;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 26px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#eye_detection_btn:hover{background-color: '#1DA1F2';"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    button2.setStyleSheet(
        "#color_detection_btn{height: 42px;"
        "margin: 15px;"
        "padding: 5px 0;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 26px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#color_detection_btn:hover{background-color: '#1DA1F2';"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    button3.setStyleSheet(
        "#object_detection_btn{height: 42px;"
        "margin: 15px;"
        "padding: 5px 0;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 26px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#object_detection_btn:hover{background-color: '#1DA1F2';"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    button1.clicked.connect(goto_frame3)
    button2.clicked.connect(goto_frame4)
    button3.clicked.connect(goto_frame5)

    backButton = QPushButton()
    backButton.setObjectName("backButton")
    backButton.setCursor(QCursor(Qt.PointingHandCursor))
    backButton.setStyleSheet(
        "#backButton{"
        "image: url(Photos/arrow_back_grey.png);"
        "background-repeat: no-repeat;"
        "width: 32px;"
        "height: 32px;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 15px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#backButton:hover{background-color: '#1DA1F2';"
        "image: url(Photos/arrow_back_white.png);"
        "background-repeat: no-repeat;"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    backButton.setFixedSize(60, 60)
    back_widget.setFixedHeight(80)
    #back_widget.setStyleSheet(
    #    "background-color: orange;"
    #)
    backButton.clicked.connect(goto_frame1)
    widgets["backButton"].append(backButton)

    # Vertical spacer
    verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    # Horizontal spacer
    horizontalSpacer = QSpacerItem(250, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    
    #grid.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding), 0,0)

    image_Layout.addItem(QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed), 0, 0)
    image_Layout.addWidget(widgets["title1"][-1], 0, 1)
    image_Layout.addWidget(widgets["title2"][-1], 0, 2)
    image_Layout.addWidget(widgets["title3"][-1], 0, 3)
    image_Layout.addItem(QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed), 0, 4)
    image_Layout.addItem(QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed), 1, 0)
    image_Layout.addWidget(widgets["image1"][-1], 1, 1)
    image_Layout.addWidget(widgets["image2"][-1], 1, 2)
    image_Layout.addWidget(widgets["image3"][-1], 1, 3)
    image_Layout.addItem(QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed), 1, 4)
    image_Layout.addItem(QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed), 2, 0)
    image_Layout.addWidget(widgets["button1"][-1], 2, 1)
    image_Layout.addWidget(widgets["button2"][-1], 2, 2)
    image_Layout.addWidget(widgets["button3"][-1], 2, 3)
    image_Layout.addItem(QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed), 2, 4)
    image_grid.setLayout(image_Layout)
    grid.addWidget(widgets["image_grid"][-1], 1, 0, 5, 0)

    #grid.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding), 2,0)
    back_horizontalLayout.addItem(QSpacerItem(15, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    back_horizontalLayout.addWidget(widgets["backButton"][-1])
    back_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    back_widget.setLayout(back_horizontalLayout)
    grid.addWidget(widgets["back_widget"][-1], 7, 0, 1, 0)


#*********************************************
#                  FRAME 3
#*********************************************
def frame3():
    window.setWindowTitle("Eye detection")
    back_horizontalLayout = QHBoxLayout()
    back_widget = QWidget()
    type_detection_horizontalLayout = QHBoxLayout()
    type_detection_widget = QWidget()
    grid_image_detect = QGridLayout()
    image_detect = QWidget()

    #type_detection_widget.setStyleSheet(
    #    "background-color: lightgreen;"
    #)
    #image_detect.setStyleSheet(
    #    "background-color: purple;"
    #)

    # Append widgets to list widgets
    widgets["back_widget"].append(back_widget)
    widgets["type_detection_widget"].append(type_detection_widget)
    widgets["image_detect"].append(image_detect)

    image_detect_btn = QPushButton("Image detection")
    video_detect_btn = QPushButton("Video detection")
    webcam_detect_btn = QPushButton("Real time detection")

    image_detect_btn.setFont(QFont(font(), 12, 700))
    video_detect_btn.setFont(QFont(font(), 12, 700))
    webcam_detect_btn.setFont(QFont(font(), 12, 700))

    widgets["image_detect_btn"].append(image_detect_btn)
    widgets["video_detect_btn"].append(video_detect_btn)
    widgets["webcam_detect_btn"].append(webcam_detect_btn)

    image_detect_btn.setObjectName("image_detect_btn")
    video_detect_btn.setObjectName("video_detect_btn")
    webcam_detect_btn.setObjectName("webcam_detect_btn")

    #icon1 = QIcon()
    #icon1.addPixmap(QPixmap("D:/Institute/First semester 2 year/APA/Example\\../Project/Photos/image_grey.png"), QIcon.Mode.Normal, QIcon.State.Off)
    #image_detect_btn.setIcon(icon1)

    image_detect_btn.setStyleSheet(
        "#image_detect_btn{height: 25px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/image_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#image_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/image_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    video_detect_btn.setStyleSheet(
        "#video_detect_btn{height: 25px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/camera_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#video_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/camera_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    webcam_detect_btn.setStyleSheet(
        "#webcam_detect_btn{height: 25px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/live_video_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#webcam_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/live_video_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )


    image_detect_btn.clicked.connect(goto_image_eye_detect)
    video_detect_btn.clicked.connect(goto_video_eye_detect)
    webcam_detect_btn.clicked.connect(goto_camera_eye_detect)


    backButton = QPushButton()
    backButton.setObjectName("backButton")
    backButton.setCursor(QCursor(Qt.PointingHandCursor))
    backButton.setStyleSheet(
        "#backButton{"
        "image: url(Photos/arrow_back_grey.png);"
        "background-repeat: no-repeat;"
        "width: 32px;"
        "height: 32px;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 15px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#backButton:hover{background-color: '#1DA1F2';"
        "image: url(Photos/arrow_back_white.png);"
        "background-repeat: no-repeat;"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    backButton.setFixedSize(60, 60)
    #back_widget.setStyleSheet(
    #    "background-color: orange;"
    #)
    backButton.clicked.connect(goto_frame2)
    widgets["backButton"].append(backButton)


    type_detection_horizontalLayout.addWidget(image_detect_btn)
    type_detection_horizontalLayout.addWidget(video_detect_btn)
    type_detection_horizontalLayout.addWidget(webcam_detect_btn)
    type_detection_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    type_detection_widget.setLayout(type_detection_horizontalLayout)
    grid.setRowStretch(0, 0)
    grid.addWidget(type_detection_widget, 0, 0, 1, 0)


    image_detect.setLayout(grid_image_detect)
    grid.setRowStretch(1, 6)
    grid.addWidget(image_detect, 1, 0, 6, 0)


    back_horizontalLayout.addItem(QSpacerItem(15, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    back_horizontalLayout.addWidget(widgets["backButton"][-1])
    back_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    back_widget.setLayout(back_horizontalLayout)
    grid.addWidget(widgets["back_widget"][-1], 7, 0)


#********************************************************************
#                  FRAME 3.1 Image eye detection
#********************************************************************
def image_eye_detect():
    
    back_horizontalLayout = QHBoxLayout()
    back_widget = QWidget()
    image_toolbar_horizontalLayout = QHBoxLayout()
    image_toolbar_widget = QWidget()
    grid_image_detect = QGridLayout()
    image_detect = QWidget()

    #image_toolbar_widget.setStyleSheet(
    #    "background-color: coral;"
    #)
    #image_detect.setStyleSheet(
    #    "background-color: lightblue;"
    #)


    # Append widgets to list widgets
    widgets["back_widget"].append(back_widget)
    widgets["image_toolbar_widget"].append(image_toolbar_widget)
    widgets["image_detect"].append(image_detect)

    image_import_btn = QPushButton("Import")
    image_download_btn = QPushButton("Download")
    image_detect_btn = QPushButton("Detect")

    image_import_btn.setFont(QFont(font(), 12, 700))
    image_download_btn.setFont(QFont(font(), 12, 700))
    image_detect_btn.setFont(QFont(font(), 12, 700))

    widgets["image_import_btn"].append(image_import_btn)
    widgets["image_download_btn"].append(image_download_btn)
    widgets["image_detect_btn"].append(image_detect_btn)

    image_import_btn.setObjectName("image_import_btn")
    image_download_btn.setObjectName("image_download_btn")
    image_detect_btn.setObjectName("image_detect_btn")

    image_import_btn.setStyleSheet(
        "#image_import_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/import_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#image_import_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/import_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    image_download_btn.setStyleSheet(
        "#image_download_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/download_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#image_download_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/download_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    image_detect_btn.setStyleSheet(
        "#image_detect_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/AI_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#image_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/AI_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    image_import_btn.clicked.connect(partial(display_image_eyes, grid_image_detect, image_detect_btn, image_download_btn))
    #image_detect_btn.clicked.connect(partial(main, image_file))
    image_download_btn.clicked.connect(saveImage_eye)


    backButton = QPushButton()
    backButton.setObjectName("backButton")
    backButton.setCursor(QCursor(Qt.PointingHandCursor))
    backButton.setStyleSheet(
        "#backButton{"
        "image: url(Photos/arrow_back_grey.png);"
        "background-repeat: no-repeat;"
        "width: 32px;"
        "height: 32px;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 15px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#backButton:hover{background-color: '#1DA1F2';"
        "image: url(Photos/arrow_back_white.png);"
        "background-repeat: no-repeat;"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    backButton.setFixedSize(60, 60)
    #back_widget.setStyleSheet(
    #    "background-color: orange;"
    #)
    backButton.clicked.connect(goto_frame2)
    widgets["backButton"].append(backButton)


    image_toolbar_horizontalLayout.addWidget(image_import_btn)
    image_toolbar_horizontalLayout.addWidget(image_download_btn)
    image_toolbar_horizontalLayout.addWidget(image_detect_btn)
    image_toolbar_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    image_toolbar_widget.setLayout(image_toolbar_horizontalLayout)
    grid.setRowStretch(0, 0)
    grid.addWidget(image_toolbar_widget, 0, 0, 1, 0)


    
    image_detect.setLayout(grid_image_detect)
    grid.setRowStretch(1, 6)
    grid.addWidget(image_detect, 1, 0, 6, 0)


    back_horizontalLayout.addItem(QSpacerItem(15, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    back_horizontalLayout.addWidget(widgets["backButton"][-1])
    back_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    back_widget.setLayout(back_horizontalLayout)
    grid.addWidget(widgets["back_widget"][-1], 7, 0)


#********************************************************************
#                  FRAME 3.2 Video eye detection
#********************************************************************
def video_eye_detect():
    
    back_horizontalLayout = QHBoxLayout()
    back_widget = QWidget()
    video_toolbar_horizontalLayout = QHBoxLayout()
    video_toolbar_widget = QWidget()
    grid_video_detect = QGridLayout()
    video_detect = QWidget()

    #video_toolbar_widget.setStyleSheet(
    #    "background-color: pink;"
    #)
    #video_detect.setStyleSheet(
    #    "background-color: coral;"
    #)


    # Append widgets to list widgets
    widgets["back_widget"].append(back_widget)
    widgets["video_toolbar_widget"].append(video_toolbar_widget)
    widgets["video_detect"].append(video_detect)

    video_import_btn = QPushButton("Import")
    video_detect_btn = QPushButton("Detect")
    video_screenshot_btn = QPushButton("Screenshot")
    video_play_btn = QPushButton("Play")
    video_stop_btn = QPushButton("Stop")

    video_import_btn.setFont(QFont(font(), 12, 700))
    video_detect_btn.setFont(QFont(font(), 12, 700))
    video_screenshot_btn.setFont(QFont(font(), 12, 700))
    video_play_btn.setFont(QFont(font(), 12, 700))
    video_stop_btn.setFont(QFont(font(), 12, 700))

    widgets["video_import_btn"].append(video_import_btn)
    widgets["video_detect_btn"].append(video_detect_btn)
    widgets["video_screenshot_btn"].append(video_screenshot_btn)
    widgets["video_play_btn"].append(video_play_btn)
    widgets["video_stop_btn"].append(video_stop_btn)

    video_import_btn.setObjectName("video_import_btn")
    video_detect_btn.setObjectName("video_detect_btn")
    video_screenshot_btn.setObjectName("video_screenshot_btn")
    video_play_btn.setObjectName("video_play_btn")
    video_stop_btn.setObjectName("video_stop_btn")

    video_import_btn.setStyleSheet(
        "#video_import_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/import_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#video_import_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/import_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    video_screenshot_btn.setStyleSheet(
        "#video_screenshot_btn{height: 25px;"
        "width: 150px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/download_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#video_screenshot_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/download_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    video_detect_btn.setStyleSheet(
        "#video_detect_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/AI_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#video_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/AI_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    video_play_btn.setStyleSheet(
        "#video_play_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/play_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#video_play_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/play_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    video_stop_btn.setStyleSheet(
        "#video_stop_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/stop_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#video_stop_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/stop_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    video_import_btn.clicked.connect(partial(display_video_eyes, grid_video_detect, video_detect_btn, video_play_btn, video_stop_btn, video_screenshot_btn))
    #video_detect_btn.clicked.connect(partial(main, image_file))
    #video_screenshot_btn.clicked.connect(Detector.saveImage)


    backButton = QPushButton()
    backButton.setObjectName("backButton")
    backButton.setCursor(QCursor(Qt.PointingHandCursor))
    backButton.setStyleSheet(
        "#backButton{"
        "image: url(Photos/arrow_back_grey.png);"
        "background-repeat: no-repeat;"
        "width: 32px;"
        "height: 32px;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 15px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#backButton:hover{background-color: '#1DA1F2';"
        "image: url(Photos/arrow_back_white.png);"
        "background-repeat: no-repeat;"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    backButton.setFixedSize(60, 60)
    #back_widget.setStyleSheet(
    #    "background-color: orange;"
    #)
    backButton.clicked.connect(goto_frame2)
    widgets["backButton"].append(backButton)


    video_toolbar_horizontalLayout.addWidget(video_import_btn)
    video_toolbar_horizontalLayout.addWidget(video_detect_btn)
    video_toolbar_horizontalLayout.addWidget(video_play_btn)
    video_toolbar_horizontalLayout.addWidget(video_stop_btn)
    video_toolbar_horizontalLayout.addWidget(video_screenshot_btn)
    video_toolbar_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    video_toolbar_widget.setLayout(video_toolbar_horizontalLayout)
    grid.setRowStretch(0, 0)
    grid.addWidget(video_toolbar_widget, 0, 0, 1, 0)


    
    video_detect.setLayout(grid_video_detect)
    grid.setRowStretch(1, 6)
    grid.addWidget(video_detect, 1, 0, 6, 0)


    back_horizontalLayout.addItem(QSpacerItem(15, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    back_horizontalLayout.addWidget(widgets["backButton"][-1])
    back_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    back_widget.setLayout(back_horizontalLayout)
    grid.addWidget(widgets["back_widget"][-1], 7, 0)


#********************************************************************
#                  FRAME 3.3 Camera eyes detection
#********************************************************************
def camera_eye_detect():
    
    back_horizontalLayout = QHBoxLayout()
    back_widget = QWidget()
    camera_toolbar_horizontalLayout = QHBoxLayout()
    camera_toolbar_widget = QWidget()
    grid_camera_detect = QGridLayout()
    camera_detect = QWidget()

    #camera_toolbar_widget.setStyleSheet(
    #    "background-color: pink;"
    #)
    #camera_detect.setStyleSheet(
    #    "background-color: coral;"
    #)


    # Append widgets to list widgets
    widgets["back_widget"].append(back_widget)
    widgets["camera_toolbar_widget"].append(camera_toolbar_widget)
    widgets["camera_detect"].append(camera_detect)

    camera_screenshot_btn = QPushButton("Screenshot")
    camera_play_btn = QPushButton("Play")
    camera_stop_btn = QPushButton("Stop")

    camera_screenshot_btn.setFont(QFont(font(), 12, 700))
    camera_play_btn.setFont(QFont(font(), 12, 700))
    camera_stop_btn.setFont(QFont(font(), 12, 700))

    widgets["camera_screenshot_btn"].append(camera_screenshot_btn)
    widgets["camera_play_btn"].append(camera_play_btn)
    widgets["camera_stop_btn"].append(camera_stop_btn)

    camera_screenshot_btn.setObjectName("camera_screenshot_btn")
    camera_play_btn.setObjectName("camera_play_btn")
    camera_stop_btn.setObjectName("camera_stop_btn")

    camera_screenshot_btn.setStyleSheet(
        "#camera_screenshot_btn{height: 25px;"
        "width: 150px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/download_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#camera_screenshot_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/download_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    camera_play_btn.setStyleSheet(
        "#camera_play_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/play_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#camera_play_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/play_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    camera_stop_btn.setStyleSheet(
        "#camera_stop_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/stop_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#camera_stop_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/stop_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    camera_play_btn.clicked.connect(partial(Camera_Detector_eyes, grid_camera_detect, camera_play_btn, camera_stop_btn, camera_screenshot_btn), Qt.ConnectionType.SingleShotConnection)
    #camera_detect_btn.clicked.connect(partial(main, image_file))
    #camera_screenshot_btn.clicked.connect(Detector.saveImage)


    backButton = QPushButton()
    backButton.setObjectName("backButton")
    backButton.setCursor(QCursor(Qt.PointingHandCursor))
    backButton.setStyleSheet(
        "#backButton{"
        "image: url(Photos/arrow_back_grey.png);"
        "background-repeat: no-repeat;"
        "width: 32px;"
        "height: 32px;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 15px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#backButton:hover{background-color: '#1DA1F2';"
        "image: url(Photos/arrow_back_white.png);"
        "background-repeat: no-repeat;"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    backButton.setFixedSize(60, 60)
    #back_widget.setStyleSheet(
    #    "background-color: orange;"
    #)
    backButton.clicked.connect(goto_frame2)
    widgets["backButton"].append(backButton)


    camera_toolbar_horizontalLayout.addWidget(camera_play_btn)
    camera_toolbar_horizontalLayout.addWidget(camera_stop_btn)
    camera_toolbar_horizontalLayout.addWidget(camera_screenshot_btn)
    camera_toolbar_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    camera_toolbar_widget.setLayout(camera_toolbar_horizontalLayout)
    grid.setRowStretch(0, 0)
    grid.addWidget(camera_toolbar_widget, 0, 0, 1, 0)


    
    camera_detect.setLayout(grid_camera_detect)
    grid.setRowStretch(1, 6)
    grid.addWidget(camera_detect, 1, 0, 6, 0)


    back_horizontalLayout.addItem(QSpacerItem(15, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    back_horizontalLayout.addWidget(widgets["backButton"][-1])
    back_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    back_widget.setLayout(back_horizontalLayout)
    grid.addWidget(widgets["back_widget"][-1], 7, 0)



#*********************************************
#                  FRAME 4
#*********************************************
def frame4():
    window.setWindowTitle("Color detection")
    back_horizontalLayout = QHBoxLayout()
    back_widget = QWidget()
    type_detection_horizontalLayout = QHBoxLayout()
    type_detection_widget = QWidget()
    grid_image_detect = QGridLayout()
    image_detect = QWidget()

    #type_detection_widget.setStyleSheet(
    #    "background-color: burgundy;"
    #)
    #image_detect.setStyleSheet(
    #    "background-color: cyan;"
    #)

    # Append widgets to list widgets
    widgets["back_widget"].append(back_widget)
    widgets["type_detection_widget"].append(type_detection_widget)
    widgets["image_detect"].append(image_detect)

    image_detect_btn = QPushButton("Image detection")
    video_detect_btn = QPushButton("Real time detection with label")
    webcam_detect_btn = QPushButton("Real time detection by click")

    image_detect_btn.setFont(QFont(font(), 12, 700))
    video_detect_btn.setFont(QFont(font(), 12, 700))
    webcam_detect_btn.setFont(QFont(font(), 12, 700))

    widgets["image_detect_btn"].append(image_detect_btn)
    widgets["video_detect_btn"].append(video_detect_btn)
    widgets["webcam_detect_btn"].append(webcam_detect_btn)

    image_detect_btn.setObjectName("image_detect_btn")
    video_detect_btn.setObjectName("video_detect_btn")
    webcam_detect_btn.setObjectName("webcam_detect_btn")

    image_detect_btn.setStyleSheet(
        "#image_detect_btn{height: 25px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/image_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#image_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/image_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    video_detect_btn.setStyleSheet(
        "#video_detect_btn{height: 25px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/live_video_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#video_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/live_video_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    webcam_detect_btn.setStyleSheet(
        "#webcam_detect_btn{height: 25px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/live_video_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#webcam_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/live_video_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    image_detect_btn.clicked.connect(goto_image_color_detect)
    video_detect_btn.clicked.connect(goto_camera_color_detect_by_label)
    webcam_detect_btn.clicked.connect(goto_camera_color_detect_by_click)


    backButton = QPushButton()
    backButton.setObjectName("backButton")
    backButton.setCursor(QCursor(Qt.PointingHandCursor))
    backButton.setStyleSheet(
        "#backButton{"
        "image: url(Photos/arrow_back_grey.png);"
        "background-repeat: no-repeat;"
        "width: 32px;"
        "height: 32px;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 15px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#backButton:hover{background-color: '#1DA1F2';"
        "image: url(Photos/arrow_back_white.png);"
        "background-repeat: no-repeat;"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    backButton.setFixedSize(60, 60)
    #back_widget.setStyleSheet(
    #    "background-color: orange;"
    #)
    backButton.clicked.connect(goto_frame2)
    widgets["backButton"].append(backButton)


    type_detection_horizontalLayout.addWidget(image_detect_btn)
    type_detection_horizontalLayout.addWidget(video_detect_btn)
    type_detection_horizontalLayout.addWidget(webcam_detect_btn)
    type_detection_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    type_detection_widget.setLayout(type_detection_horizontalLayout)
    grid.setRowStretch(0, 0)
    grid.addWidget(type_detection_widget, 0, 0, 1, 0)


    image_detect.setLayout(grid_image_detect)
    grid.setRowStretch(1, 6)
    grid.addWidget(image_detect, 1, 0, 6, 0)


    back_horizontalLayout.addItem(QSpacerItem(15, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    back_horizontalLayout.addWidget(widgets["backButton"][-1])
    back_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    back_widget.setLayout(back_horizontalLayout)
    grid.addWidget(widgets["back_widget"][-1], 7, 0)


#********************************************************************
#                  FRAME 4.1 Image color detection
#********************************************************************
def image_color_detect():
    
    back_horizontalLayout = QHBoxLayout()
    back_widget = QWidget()
    image_toolbar_horizontalLayout = QHBoxLayout()
    image_toolbar_widget = QWidget()
    grid_image_detect = QGridLayout()
    image_detect = QWidget()

    #image_toolbar_widget.setStyleSheet(
    #    "background-color: lightblue;"
    #)
    #image_detect.setStyleSheet(
    #    "background-color: lightgreen;"
    #)


    # Append widgets to list widgets
    widgets["back_widget"].append(back_widget)
    widgets["image_toolbar_widget"].append(image_toolbar_widget)
    widgets["image_detect"].append(image_detect)

    image_import_btn = QPushButton("Import")
    image_download_btn = QPushButton("Download")
    image_detect_btn = QPushButton("Detect")

    image_import_btn.setFont(QFont(font(), 12, 700))
    image_download_btn.setFont(QFont(font(), 12, 700))
    image_detect_btn.setFont(QFont(font(), 12, 700))

    widgets["image_import_btn"].append(image_import_btn)
    widgets["image_download_btn"].append(image_download_btn)
    widgets["image_detect_btn"].append(image_detect_btn)

    image_import_btn.setObjectName("image_import_btn")
    image_download_btn.setObjectName("image_download_btn")
    image_detect_btn.setObjectName("image_detect_btn")

    image_import_btn.setStyleSheet(
        "#image_import_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/import_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#image_import_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/import_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    image_download_btn.setStyleSheet(
        "#image_download_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/download_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#image_download_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/download_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    image_detect_btn.setStyleSheet(
        "#image_detect_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/AI_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#image_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/AI_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    image_import_btn.clicked.connect(partial(display_image_color, grid_image_detect, image_detect_btn, image_download_btn))
    #image_detect_btn.clicked.connect(partial(main, image_file))
    image_download_btn.clicked.connect(saveImage_color)


    backButton = QPushButton()
    backButton.setObjectName("backButton")
    backButton.setCursor(QCursor(Qt.PointingHandCursor))
    backButton.setStyleSheet(
        "#backButton{"
        "image: url(Photos/arrow_back_grey.png);"
        "background-repeat: no-repeat;"
        "width: 32px;"
        "height: 32px;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 15px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#backButton:hover{background-color: '#1DA1F2';"
        "image: url(Photos/arrow_back_white.png);"
        "background-repeat: no-repeat;"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    backButton.setFixedSize(60, 60)
    #back_widget.setStyleSheet(
    #    "background-color: orange;"
    #)
    backButton.clicked.connect(goto_frame2)
    widgets["backButton"].append(backButton)


    image_toolbar_horizontalLayout.addWidget(image_import_btn)
    image_toolbar_horizontalLayout.addWidget(image_download_btn)
    image_toolbar_horizontalLayout.addWidget(image_detect_btn)
    image_toolbar_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    image_toolbar_widget.setLayout(image_toolbar_horizontalLayout)
    grid.setRowStretch(0, 0)
    grid.addWidget(image_toolbar_widget, 0, 0, 1, 0)


    
    image_detect.setLayout(grid_image_detect)
    grid.setRowStretch(1, 6)
    grid.addWidget(image_detect, 1, 0, 6, 0)


    back_horizontalLayout.addItem(QSpacerItem(15, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    back_horizontalLayout.addWidget(widgets["backButton"][-1])
    back_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    back_widget.setLayout(back_horizontalLayout)
    grid.addWidget(widgets["back_widget"][-1], 7, 0)


#********************************************************************
#                  FRAME 4.2 Camera color detection by label
#********************************************************************
def camera_color_detect_by_label():
    
    back_horizontalLayout = QHBoxLayout()
    back_widget = QWidget()
    camera_toolbar_horizontalLayout = QHBoxLayout()
    camera_toolbar_widget = QWidget()
    grid_camera_detect = QGridLayout()
    camera_detect = QWidget()

    #camera_toolbar_widget.setStyleSheet(
    #    "background-color: pink;"
    #)
    #camera_detect.setStyleSheet(
    #    "background-color: coral;"
    #)


    # Append widgets to list widgets
    widgets["back_widget"].append(back_widget)
    widgets["camera_toolbar_widget"].append(camera_toolbar_widget)
    widgets["camera_detect"].append(camera_detect)

    camera_screenshot_btn = QPushButton("Screenshot")
    camera_play_btn = QPushButton("Play")
    camera_stop_btn = QPushButton("Stop")

    camera_screenshot_btn.setFont(QFont(font(), 12, 700))
    camera_play_btn.setFont(QFont(font(), 12, 700))
    camera_stop_btn.setFont(QFont(font(), 12, 700))

    widgets["camera_screenshot_btn"].append(camera_screenshot_btn)
    widgets["camera_play_btn"].append(camera_play_btn)
    widgets["camera_stop_btn"].append(camera_stop_btn)

    camera_screenshot_btn.setObjectName("camera_screenshot_btn")
    camera_play_btn.setObjectName("camera_play_btn")
    camera_stop_btn.setObjectName("camera_stop_btn")

    camera_screenshot_btn.setStyleSheet(
        "#camera_screenshot_btn{height: 25px;"
        "width: 150px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/download_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#camera_screenshot_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/download_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    camera_play_btn.setStyleSheet(
        "#camera_play_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/play_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#camera_play_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/play_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    camera_stop_btn.setStyleSheet(
        "#camera_stop_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/stop_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#camera_stop_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/stop_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    camera_play_btn.clicked.connect(partial(Camera_color_detect_label, grid_camera_detect, camera_play_btn, camera_stop_btn, camera_screenshot_btn), Qt.ConnectionType.SingleShotConnection)
    #camera_detect_btn.clicked.connect(partial(main, image_file))
    #camera_screenshot_btn.clicked.connect(Detector.saveImage)


    backButton = QPushButton()
    backButton.setObjectName("backButton")
    backButton.setCursor(QCursor(Qt.PointingHandCursor))
    backButton.setStyleSheet(
        "#backButton{"
        "image: url(Photos/arrow_back_grey.png);"
        "background-repeat: no-repeat;"
        "width: 32px;"
        "height: 32px;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 15px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#backButton:hover{background-color: '#1DA1F2';"
        "image: url(Photos/arrow_back_white.png);"
        "background-repeat: no-repeat;"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    backButton.setFixedSize(60, 60)
    #back_widget.setStyleSheet(
    #    "background-color: orange;"
    #)
    backButton.clicked.connect(goto_frame2)
    widgets["backButton"].append(backButton)


    camera_toolbar_horizontalLayout.addWidget(camera_play_btn)
    camera_toolbar_horizontalLayout.addWidget(camera_stop_btn)
    camera_toolbar_horizontalLayout.addWidget(camera_screenshot_btn)
    camera_toolbar_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    camera_toolbar_widget.setLayout(camera_toolbar_horizontalLayout)
    grid.setRowStretch(0, 0)
    grid.addWidget(camera_toolbar_widget, 0, 0, 1, 0)


    
    camera_detect.setLayout(grid_camera_detect)
    grid.setRowStretch(1, 6)
    grid.addWidget(camera_detect, 1, 0, 6, 0)


    back_horizontalLayout.addItem(QSpacerItem(15, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    back_horizontalLayout.addWidget(widgets["backButton"][-1])
    back_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    back_widget.setLayout(back_horizontalLayout)
    grid.addWidget(widgets["back_widget"][-1], 7, 0)


#********************************************************************
#                  FRAME 4.3 Camera color detection by click
#********************************************************************
def camera_color_detect_by_click():
    
    back_horizontalLayout = QHBoxLayout()
    back_widget = QWidget()
    camera_toolbar_horizontalLayout = QHBoxLayout()
    camera_toolbar_widget = QWidget()
    grid_camera_detect = QGridLayout()
    camera_detect = QWidget()

    #camera_toolbar_widget.setStyleSheet(
    #    "background-color: pink;"
    #)
    #camera_detect.setStyleSheet(
    #    "background-color: coral;"
    #)


    # Append widgets to list widgets
    widgets["back_widget"].append(back_widget)
    widgets["camera_toolbar_widget"].append(camera_toolbar_widget)
    widgets["camera_detect"].append(camera_detect)

    camera_screenshot_btn = QPushButton("Screenshot")
    camera_play_btn = QPushButton("Play")
    camera_stop_btn = QPushButton("Stop")

    camera_screenshot_btn.setFont(QFont(font(), 12, 700))
    camera_play_btn.setFont(QFont(font(), 12, 700))
    camera_stop_btn.setFont(QFont(font(), 12, 700))

    widgets["camera_screenshot_btn"].append(camera_screenshot_btn)
    widgets["camera_play_btn"].append(camera_play_btn)
    widgets["camera_stop_btn"].append(camera_stop_btn)

    camera_screenshot_btn.setObjectName("camera_screenshot_btn")
    camera_play_btn.setObjectName("camera_play_btn")
    camera_stop_btn.setObjectName("camera_stop_btn")

    camera_screenshot_btn.setStyleSheet(
        "#camera_screenshot_btn{height: 25px;"
        "width: 150px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/download_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#camera_screenshot_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/download_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    camera_play_btn.setStyleSheet(
        "#camera_play_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/play_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#camera_play_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/play_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    camera_stop_btn.setStyleSheet(
        "#camera_stop_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/stop_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#camera_stop_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/stop_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    camera_play_btn.clicked.connect(partial(Camera_color_detect_click, grid_camera_detect, camera_play_btn, camera_stop_btn, camera_screenshot_btn), Qt.ConnectionType.SingleShotConnection)
    #camera_detect_btn.clicked.connect(partial(main, image_file))
    #camera_screenshot_btn.clicked.connect(Detector.saveImage)


    backButton = QPushButton()
    backButton.setObjectName("backButton")
    backButton.setCursor(QCursor(Qt.PointingHandCursor))
    backButton.setStyleSheet(
        "#backButton{"
        "image: url(Photos/arrow_back_grey.png);"
        "background-repeat: no-repeat;"
        "width: 32px;"
        "height: 32px;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 15px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#backButton:hover{background-color: '#1DA1F2';"
        "image: url(Photos/arrow_back_white.png);"
        "background-repeat: no-repeat;"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    backButton.setFixedSize(60, 60)
    #back_widget.setStyleSheet(
    #    "background-color: orange;"
    #)
    backButton.clicked.connect(goto_frame2)
    widgets["backButton"].append(backButton)


    camera_toolbar_horizontalLayout.addWidget(camera_play_btn)
    camera_toolbar_horizontalLayout.addWidget(camera_stop_btn)
    camera_toolbar_horizontalLayout.addWidget(camera_screenshot_btn)
    camera_toolbar_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    camera_toolbar_widget.setLayout(camera_toolbar_horizontalLayout)
    grid.setRowStretch(0, 0)
    grid.addWidget(camera_toolbar_widget, 0, 0, 1, 0)


    
    camera_detect.setLayout(grid_camera_detect)
    grid.setRowStretch(1, 6)
    grid.addWidget(camera_detect, 1, 0, 6, 0)


    back_horizontalLayout.addItem(QSpacerItem(15, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    back_horizontalLayout.addWidget(widgets["backButton"][-1])
    back_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    back_widget.setLayout(back_horizontalLayout)
    grid.addWidget(widgets["back_widget"][-1], 7, 0)



#*********************************************
#                  FRAME 5
#*********************************************
def frame5():
    window.setWindowTitle("Object detection")
    back_horizontalLayout = QHBoxLayout()
    back_widget = QWidget()
    type_detection_horizontalLayout = QHBoxLayout()
    type_detection_widget = QWidget()
    grid_image_detect = QGridLayout()
    image_detect = QWidget()

    #type_detection_widget.setStyleSheet(
    #    "background-color: pink;"
    #)
    #image_detect.setStyleSheet(
    #    "background-color: coral;"
    #)

    # Append widgets to list widgets
    widgets["back_widget"].append(back_widget)
    widgets["type_detection_widget"].append(type_detection_widget)
    widgets["image_detect"].append(image_detect)

    image_detect_btn = QPushButton("Image detection")
    video_detect_btn = QPushButton("Video detection")
    webcam_detect_btn = QPushButton("Real time detection")

    image_detect_btn.setFont(QFont(font(), 12, 700))
    video_detect_btn.setFont(QFont(font(), 12, 700))
    webcam_detect_btn.setFont(QFont(font(), 12, 700))

    widgets["image_detect_btn"].append(image_detect_btn)
    widgets["video_detect_btn"].append(video_detect_btn)
    widgets["webcam_detect_btn"].append(webcam_detect_btn)

    image_detect_btn.setObjectName("image_detect_btn")
    video_detect_btn.setObjectName("video_detect_btn")
    webcam_detect_btn.setObjectName("webcam_detect_btn")

    image_detect_btn.setStyleSheet(
        "#image_detect_btn{height: 25px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/image_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#image_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/image_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    video_detect_btn.setStyleSheet(
        "#video_detect_btn{height: 25px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/camera_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#video_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/camera_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    webcam_detect_btn.setStyleSheet(
        "#webcam_detect_btn{height: 25px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/live_video_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#webcam_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/live_video_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    image_detect_btn.clicked.connect(goto_image_obj_detect)
    video_detect_btn.clicked.connect(goto_video_obj_detect)
    webcam_detect_btn.clicked.connect(goto_camera_obj_detect)


    backButton = QPushButton()
    backButton.setObjectName("backButton")
    backButton.setCursor(QCursor(Qt.PointingHandCursor))
    backButton.setStyleSheet(
        "#backButton{"
        "image: url(Photos/arrow_back_grey.png);"
        "background-repeat: no-repeat;"
        "width: 32px;"
        "height: 32px;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 15px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#backButton:hover{background-color: '#1DA1F2';"
        "image: url(Photos/arrow_back_white.png);"
        "background-repeat: no-repeat;"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    backButton.setFixedSize(60, 60)
    #back_widget.setStyleSheet(
    #    "background-color: orange;"
    #)
    backButton.clicked.connect(goto_frame2)
    widgets["backButton"].append(backButton)


    type_detection_horizontalLayout.addWidget(image_detect_btn)
    type_detection_horizontalLayout.addWidget(video_detect_btn)
    type_detection_horizontalLayout.addWidget(webcam_detect_btn)
    type_detection_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    type_detection_widget.setLayout(type_detection_horizontalLayout)
    grid.setRowStretch(0, 0)
    grid.addWidget(type_detection_widget, 0, 0, 1, 0)


    image_detect.setLayout(grid_image_detect)
    grid.setRowStretch(1, 6)
    grid.addWidget(image_detect, 1, 0, 6, 0)


    back_horizontalLayout.addItem(QSpacerItem(15, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    back_horizontalLayout.addWidget(widgets["backButton"][-1])
    back_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    back_widget.setLayout(back_horizontalLayout)
    grid.addWidget(widgets["back_widget"][-1], 7, 0)


#********************************************************************
#                  FRAME 5.1 Image object detection
#********************************************************************
def image_obj_detect():
    
    back_horizontalLayout = QHBoxLayout()
    back_widget = QWidget()
    image_toolbar_horizontalLayout = QHBoxLayout()
    image_toolbar_widget = QWidget()
    grid_image_detect = QGridLayout()
    image_detect = QWidget()

    #image_toolbar_widget.setStyleSheet(
    #    "background-color: pink;"
    #)
    #image_detect.setStyleSheet(
    #    "background-color: coral;"
    #)


    # Append widgets to list widgets
    widgets["back_widget"].append(back_widget)
    widgets["image_toolbar_widget"].append(image_toolbar_widget)
    widgets["image_detect"].append(image_detect)

    image_import_btn = QPushButton("Import")
    image_download_btn = QPushButton("Download")
    image_detect_btn = QPushButton("Detect")

    image_import_btn.setFont(QFont(font(), 12, 700))
    image_download_btn.setFont(QFont(font(), 12, 700))
    image_detect_btn.setFont(QFont(font(), 12, 700))

    widgets["image_import_btn"].append(image_import_btn)
    widgets["image_download_btn"].append(image_download_btn)
    widgets["image_detect_btn"].append(image_detect_btn)

    image_import_btn.setObjectName("image_import_btn")
    image_download_btn.setObjectName("image_download_btn")
    image_detect_btn.setObjectName("image_detect_btn")

    image_import_btn.setStyleSheet(
        "#image_import_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/import_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#image_import_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/import_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    image_download_btn.setStyleSheet(
        "#image_download_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/download_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#image_download_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/download_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    image_detect_btn.setStyleSheet(
        "#image_detect_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/AI_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#image_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/AI_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    image_import_btn.clicked.connect(partial(display_image_obj, grid_image_detect, image_detect_btn, image_download_btn))
    #image_detect_btn.clicked.connect(partial(main, image_file))
    image_download_btn.clicked.connect(Image_Detector_obj.saveImage)


    backButton = QPushButton()
    backButton.setObjectName("backButton")
    backButton.setCursor(QCursor(Qt.PointingHandCursor))
    backButton.setStyleSheet(
        "#backButton{"
        "image: url(Photos/arrow_back_grey.png);"
        "background-repeat: no-repeat;"
        "width: 32px;"
        "height: 32px;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 15px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#backButton:hover{background-color: '#1DA1F2';"
        "image: url(Photos/arrow_back_white.png);"
        "background-repeat: no-repeat;"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    backButton.setFixedSize(60, 60)
    #back_widget.setStyleSheet(
    #    "background-color: orange;"
    #)
    backButton.clicked.connect(goto_frame2)
    widgets["backButton"].append(backButton)


    image_toolbar_horizontalLayout.addWidget(image_import_btn)
    image_toolbar_horizontalLayout.addWidget(image_download_btn)
    image_toolbar_horizontalLayout.addWidget(image_detect_btn)
    image_toolbar_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    image_toolbar_widget.setLayout(image_toolbar_horizontalLayout)
    grid.setRowStretch(0, 0)
    grid.addWidget(image_toolbar_widget, 0, 0, 1, 0)


    
    image_detect.setLayout(grid_image_detect)
    grid.setRowStretch(1, 6)
    grid.addWidget(image_detect, 1, 0, 6, 0)


    back_horizontalLayout.addItem(QSpacerItem(15, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    back_horizontalLayout.addWidget(widgets["backButton"][-1])
    back_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    back_widget.setLayout(back_horizontalLayout)
    grid.addWidget(widgets["back_widget"][-1], 7, 0)


#********************************************************************
#                  FRAME 5.2 Video object detection
#********************************************************************
def video_obj_detect():
    
    back_horizontalLayout = QHBoxLayout()
    back_widget = QWidget()
    video_toolbar_horizontalLayout = QHBoxLayout()
    video_toolbar_widget = QWidget()
    grid_video_detect = QGridLayout()
    video_detect = QWidget()

    #video_toolbar_widget.setStyleSheet(
    #    "background-color: pink;"
    #)
    #video_detect.setStyleSheet(
    #    "background-color: coral;"
    #)


    # Append widgets to list widgets
    widgets["back_widget"].append(back_widget)
    widgets["video_toolbar_widget"].append(video_toolbar_widget)
    widgets["video_detect"].append(video_detect)

    video_import_btn = QPushButton("Import")
    video_detect_btn = QPushButton("Detect")
    video_screenshot_btn = QPushButton("Screenshot")
    video_play_btn = QPushButton("Play")
    video_stop_btn = QPushButton("Stop")

    video_import_btn.setFont(QFont(font(), 12, 700))
    video_detect_btn.setFont(QFont(font(), 12, 700))
    video_screenshot_btn.setFont(QFont(font(), 12, 700))
    video_play_btn.setFont(QFont(font(), 12, 700))
    video_stop_btn.setFont(QFont(font(), 12, 700))

    widgets["video_import_btn"].append(video_import_btn)
    widgets["video_detect_btn"].append(video_detect_btn)
    widgets["video_screenshot_btn"].append(video_screenshot_btn)
    widgets["video_play_btn"].append(video_play_btn)
    widgets["video_stop_btn"].append(video_stop_btn)

    video_import_btn.setObjectName("video_import_btn")
    video_detect_btn.setObjectName("video_detect_btn")
    video_screenshot_btn.setObjectName("video_screenshot_btn")
    video_play_btn.setObjectName("video_play_btn")
    video_stop_btn.setObjectName("video_stop_btn")

    video_import_btn.setStyleSheet(
        "#video_import_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/import_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#video_import_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/import_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    video_screenshot_btn.setStyleSheet(
        "#video_screenshot_btn{height: 25px;"
        "width: 150px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/download_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#video_screenshot_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/download_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    video_detect_btn.setStyleSheet(
        "#video_detect_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/AI_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#video_detect_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/AI_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    video_play_btn.setStyleSheet(
        "#video_play_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/play_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#video_play_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/play_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    video_stop_btn.setStyleSheet(
        "#video_stop_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/stop_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#video_stop_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/stop_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    video_import_btn.clicked.connect(partial(display_video_obj, grid_video_detect, video_detect_btn, video_play_btn, video_stop_btn, video_screenshot_btn))
    #video_detect_btn.clicked.connect(partial(main, image_file))
    #video_screenshot_btn.clicked.connect(Detector.saveImage)


    backButton = QPushButton()
    backButton.setObjectName("backButton")
    backButton.setCursor(QCursor(Qt.PointingHandCursor))
    backButton.setStyleSheet(
        "#backButton{"
        "image: url(Photos/arrow_back_grey.png);"
        "background-repeat: no-repeat;"
        "width: 32px;"
        "height: 32px;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 15px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#backButton:hover{background-color: '#1DA1F2';"
        "image: url(Photos/arrow_back_white.png);"
        "background-repeat: no-repeat;"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    backButton.setFixedSize(60, 60)
    #back_widget.setStyleSheet(
    #    "background-color: orange;"
    #)
    backButton.clicked.connect(goto_frame2)
    widgets["backButton"].append(backButton)


    video_toolbar_horizontalLayout.addWidget(video_import_btn)
    video_toolbar_horizontalLayout.addWidget(video_detect_btn)
    video_toolbar_horizontalLayout.addWidget(video_play_btn)
    video_toolbar_horizontalLayout.addWidget(video_stop_btn)
    video_toolbar_horizontalLayout.addWidget(video_screenshot_btn)
    video_toolbar_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    video_toolbar_widget.setLayout(video_toolbar_horizontalLayout)
    grid.setRowStretch(0, 0)
    grid.addWidget(video_toolbar_widget, 0, 0, 1, 0)


    
    video_detect.setLayout(grid_video_detect)
    grid.setRowStretch(1, 6)
    grid.addWidget(video_detect, 1, 0, 6, 0)


    back_horizontalLayout.addItem(QSpacerItem(15, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    back_horizontalLayout.addWidget(widgets["backButton"][-1])
    back_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    back_widget.setLayout(back_horizontalLayout)
    grid.addWidget(widgets["back_widget"][-1], 7, 0)


#********************************************************************
#                  FRAME 5.3 Camera object detection
#********************************************************************
def camera_obj_detect():
    
    back_horizontalLayout = QHBoxLayout()
    back_widget = QWidget()
    camera_toolbar_horizontalLayout = QHBoxLayout()
    camera_toolbar_widget = QWidget()
    grid_camera_detect = QGridLayout()
    camera_detect = QWidget()

    #camera_toolbar_widget.setStyleSheet(
    #    "background-color: pink;"
    #)
    #camera_detect.setStyleSheet(
    #    "background-color: coral;"
    #)


    # Append widgets to list widgets
    widgets["back_widget"].append(back_widget)
    widgets["camera_toolbar_widget"].append(camera_toolbar_widget)
    widgets["camera_detect"].append(camera_detect)

    camera_screenshot_btn = QPushButton("Screenshot")
    camera_play_btn = QPushButton("Play")
    camera_stop_btn = QPushButton("Stop")

    camera_screenshot_btn.setFont(QFont(font(), 12, 700))
    camera_play_btn.setFont(QFont(font(), 12, 700))
    camera_stop_btn.setFont(QFont(font(), 12, 700))

    widgets["camera_screenshot_btn"].append(camera_screenshot_btn)
    widgets["camera_play_btn"].append(camera_play_btn)
    widgets["camera_stop_btn"].append(camera_stop_btn)

    camera_screenshot_btn.setObjectName("camera_screenshot_btn")
    camera_play_btn.setObjectName("camera_play_btn")
    camera_stop_btn.setObjectName("camera_stop_btn")

    camera_screenshot_btn.setStyleSheet(
        "#camera_screenshot_btn{height: 25px;"
        "width: 150px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/download_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#camera_screenshot_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/download_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    camera_play_btn.setStyleSheet(
        "#camera_play_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/play_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#camera_play_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/play_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )
    camera_stop_btn.setStyleSheet(
        "#camera_stop_btn{height: 25px;"
        "width: 100px;"
        "margin: 10px 15px;"
        "padding: 5px 10px;"
        "qproperty-icon: url(Photos/stop_grey.png);"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 10px;"
        "font-style: italic;"
        "color: '#657786';}"
        # Hover effect
        "#camera_stop_btn:hover{background-color: '#1DA1F2';"
        "qproperty-icon: url(Photos/stop_white.png);"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    camera_play_btn.clicked.connect(partial(main_camera_obj, grid_camera_detect, camera_play_btn, camera_stop_btn, camera_screenshot_btn), Qt.ConnectionType.SingleShotConnection)
    #camera_detect_btn.clicked.connect(partial(main, image_file))
    #camera_screenshot_btn.clicked.connect(Detector.saveImage)


    backButton = QPushButton()
    backButton.setObjectName("backButton")
    backButton.setCursor(QCursor(Qt.PointingHandCursor))
    backButton.setStyleSheet(
        "#backButton{"
        "image: url(Photos/arrow_back_grey.png);"
        "background-repeat: no-repeat;"
        "width: 32px;"
        "height: 32px;"
        "background-color: '#FFFFFF';"
        "border: 3px solid '#1DA1F2';"
        "border-radius: 15px;"
        "font-size: 28px;"
        "color: '#657786';}"
        # Hover effect
        "#backButton:hover{background-color: '#1DA1F2';"
        "image: url(Photos/arrow_back_white.png);"
        "background-repeat: no-repeat;"
        "border: none;"
        "color: '#FFFFFF';}"
    )

    backButton.setFixedSize(60, 60)
    #back_widget.setStyleSheet(
    #    "background-color: orange;"
    #)
    backButton.clicked.connect(goto_frame2)
    widgets["backButton"].append(backButton)


    camera_toolbar_horizontalLayout.addWidget(camera_play_btn)
    camera_toolbar_horizontalLayout.addWidget(camera_stop_btn)
    camera_toolbar_horizontalLayout.addWidget(camera_screenshot_btn)
    camera_toolbar_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    camera_toolbar_widget.setLayout(camera_toolbar_horizontalLayout)
    grid.setRowStretch(0, 0)
    grid.addWidget(camera_toolbar_widget, 0, 0, 1, 0)


    
    camera_detect.setLayout(grid_camera_detect)
    grid.setRowStretch(1, 6)
    grid.addWidget(camera_detect, 1, 0, 6, 0)


    back_horizontalLayout.addItem(QSpacerItem(15, 15, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
    back_horizontalLayout.addWidget(widgets["backButton"][-1])
    back_horizontalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    back_widget.setLayout(back_horizontalLayout)
    grid.addWidget(widgets["back_widget"][-1], 7, 0)









if __name__ == "__main__":
    app = QApplication(sys.argv)
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    window = QWidget()
    icon = QIcon()
    icon.addFile(u"Photos/Icon.png", QSize(), QIcon.Normal, QIcon.Off)
    window.setWindowIcon(icon)
    window.resize(1200, 900)
    window.setStyleSheet("background: #FFFFFF;")

    frame1()

    window.setLayout(grid)

    window.show()   
    sys.exit(app.exec())
