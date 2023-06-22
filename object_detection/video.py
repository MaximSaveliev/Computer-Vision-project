from object_detection.video_detector import *
import os

videoPath = ""

def main_video_obj(videoPath, grid_video_detect, video_play_btn, video_stop_btn, video_screenshot_btn):
    rootDirectory = os.path.dirname(__file__)
    
    #videoPath = os.path.join(rootDirectory, "videos", "C:\\Users\\Max\\Downloads\\videos\\Running - 294.mp4")
    configPath = os.path.join(rootDirectory, "data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join(rootDirectory, "data", "frozen_inference_graph.pb")
    classesPath = os.path.join(rootDirectory, "data", "coco.names")

    Video_Detector_obj(videoPath[0], configPath, modelPath, classesPath, grid_video_detect, video_play_btn, video_stop_btn, video_screenshot_btn)
    #detector.onVideo(grid_video_detect)

if __name__== '__main__':
    main_video_obj()