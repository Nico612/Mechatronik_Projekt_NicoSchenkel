import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics import YOLO
import time

#from robotiq3f_py.robotiqcontrol.GripperController import GripperController

#from robotiq3f_py.robotiqcontrol.GripperController import GripperController 
#from cam import cama
#from depthTracking import closing
#from depthTracking import gripTrigger

x = 424
y = 240

xCenter = x//2
yCenter = y//2

pipeline = rs.pipeline()
config = rs.config()
filter = rs.decimation_filter()
config.enable_stream(rs.stream.depth, x,y, rs.format.z16, 30)
config.enable_stream(rs.stream.color, x,y, rs.format.bgr8, 30)  # bgr is compatible with OpenCV 
pipelineProfile = pipeline.start(config)

# Align streams
align_to = rs.stream.color
align = rs.align(align_to)


# Set high accuracy mode
depth_sensor = pipelineProfile.get_device().first_depth_sensor()
depth_sensor.set_option(rs.option.visual_preset, rs.rs400_visual_preset.high_density)
#depth_sensor.set_option(rs.option.visual_preset, rs.rs400_visual_preset.medium_density)
depthScale = depth_sensor.get_depth_scale()
#filter = rs.decimation_filter()
# bgr is compatible with OpenCV 

arraySize = 5

#depth_sensor.set_option(rs.option.visual_preset, rs.rs400_visual_preset.medium_density)
#depthScale = depth_sensor.get_depth_scale()


while True:
    # Get images
    frames = pipeline.wait_for_frames()
    # Align the depth frame to color frame
    aligned_frames = align.process(frames)

    depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
    color_frame = aligned_frames.get_color_frame()

    if not depth_frame or not color_frame:
        continue

    color_img = np.asanyarray(color_frame.get_data())
    #depth_img = np.asanyarray(depth_frame.get_data())
    color_img1 = color_img.copy()


    profile = depth_frame.get_profile()
    intrinsics = profile.as_video_stream_profile().get_intrinsics()

    zArray = np.asanyarray(depth_frame.get_data())
    z1 = zArray[yCenter - arraySize:y + arraySize, xCenter - arraySize: x + arraySize]
    z1 = np.median(z1) * depthScale



    cv2.rectangle(color_img, (xCenter-arraySize, yCenter-arraySize), (xCenter+arraySize, yCenter+arraySize), (255,0,0), 2)
    #cv2.circle(color_img, (240,212), 10, (255,255,255), 2) , (255,0,0),2
    cv2.putText(color_img, f'dist:{z1:.2f}', (320,200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.imshow( 'test',color_img)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q') or key == 27:
        break