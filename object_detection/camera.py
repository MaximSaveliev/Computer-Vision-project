from object_detection.camera_detector import *
import os

def main_camera_obj(grid_camera_detect, camera_play_btn, camera_stop_btn, camera_screenshot_btn):
    rootDirectory = os.path.dirname(__file__)
    
    configPath = os.path.join(rootDirectory, "data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join(rootDirectory, "data", "frozen_inference_graph.pb")
    classesPath = os.path.join(rootDirectory, "data", "coco.names")

    Camera_Detector_obj(configPath, modelPath, classesPath, grid_camera_detect, camera_play_btn, camera_stop_btn, camera_screenshot_btn)
    #detector.onVideo(grid_camera_detect)

if __name__== '__main__':
    main_camera_obj()