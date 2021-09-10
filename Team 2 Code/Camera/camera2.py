## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import cv2
import imageio
import numpy as np
import pyrealsense2.pyrealsense2 as rs
import os
import shutil
import admin as a
import math
import time
import pwm_motor_controller as turning

# Darkness of a pixel that will be considered a detected object
distance_threshold = 20
turning.setup()
turning.percentage(2, 0, 0)

def detectObstacle(image, imageHeight, imageWidth):
    '''
    Scans the center row of the down scaled image and determines which direction to turn based upon the distance_threshold
    Goes straight if none the scanned pixels are below the distance_threshold
    '''
    for i in range(0, imageWidth//3):
        if((image[imageHeight//2][(imageWidth//2) + i + 1] <= distance_threshold).all()):
            return 1
        elif((image[imageHeight//2][(imageWidth//2) - i - 1] <= distance_threshold).all()):
            return 2
    return 0

def make_clean_folder(path_folder):
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)
    else:
        user_input = input("%s not empty. Overwrite? (y/n) : " % path_folder)
        if user_input.lower() == "y":
            shutil.rmtree(path_folder)
            os.makedirs(path_folder)
        else:
            exit()

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
try:
    pipeline.start(config)
except:
    print('No camera found')


make_clean_folder("../data/realsense/")
def cameraFeed():
    # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            return 0

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)


        # Print in black and white
        depth_grayscale = cv2.convertScaleAbs(depth_image, alpha=0.03)

        # Stack both images horizontally
        # Used for real-time camera feed display
        # images = np.hstack((color_image, depth_colormap))

        # imageio.imwrite("../data/realsense/depth.png", images)
        # imageio.imwrite("../data/realsense/one.png", depth_colormap)
        # imageio.imwrite("../data/realsense/three.png", color_image)

        imageio.imwrite("../data/realsense/grayscale.png", depth_grayscale)

        disparity = cv2.imread('../data/realsense/grayscale.png', 0)
        height = 12
        width = 10
        down_scaled = cv2.resize(disparity,(width,height))

        imageio.imwrite("../data/realsense/down_scaled.png", down_scaled)

        direction = detectObstacle(down_scaled, height, width)

        # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        # cv2.imshow('RealSense', images)

        #0 = straight, 1 = left, 2 = right
        if(direction != 0):
            if direction == 1:
                turning.percentage(1,0,50)
                turning.percentage(0,1,50)
                print("go left")
                return 1
            else:
                turning.percentage(1,1,50)
                turning.percentage(0,0,50)
                print("go right")
                return 2
        else:
            print("go straight")
            turning.percentage(2, 0, 50)
            return 0

while True:
    cameraFeed()

# try:
#     make_clean_folder("../data/realsense/")
#     while True:
#         # Wait for a coherent pair of frames: depth and color
#         frames = pipeline.wait_for_frames()
#         depth_frame = frames.get_depth_frame()
#         color_frame = frames.get_color_frame()
#         if not depth_frame or not color_frame:
#             continue

#         # Convert images to numpy arrays
#         depth_image = np.asanyarray(depth_frame.get_data())

#         # Apply colormap on depth image (image must be converted to 8-bit per pixel first)

#         # Print in black and white
#         depth_grayscale = cv2.convertScaleAbs(depth_image, alpha=0.03)

#         # Stack both images horizontally
#         # Used for real-time camera feed display

#         imageio.imwrite("../data/realsense/grayscale.png", depth_grayscale)

#         disparity = cv2.imread('../data/realsense/grayscale.png', 0)
#         height = 12
#         width = 10
#         down_scaled = cv2.resize(disparity,(width,height))
        
#         imageio.imwrite("../data/realsense/down_scaled.png", down_scaled)

#         direction = detectObstacle(down_scaled, height, width)

#         #0 = straight, 1 = left, 2 = right
#         if(direction != 0):
#             if direction == 1:
#                 turning.percentage(2,0,0)
#                 print("go left")
#             else:
#                 turning.percentage(2,0,0)
#                 print("go right")
#         else:
#             print("go straight")
#             turning.percentage(2, 1, 50)
        
#         # Show images
#         key = cv2.waitKey(1) & 0xFF

# finally:
#     # Stop streaming
#     pipeline.stop()