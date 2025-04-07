import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics import YOLO
import time
import csv
import os
from joblib import load


out = 0
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 424, 240, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 424, 240, rs.format.bgr8, 30)  # bgr is compatible with OpenCV

align_to = rs.stream.depth
align = rs.align(align_to)




xBasic = 300
yBasic = 30

xScissor = 80
yScissor = 20
#pipeline.start(config)
pipelineProfile = pipeline.start(config)

depth_sensor = pipelineProfile.get_device().first_depth_sensor()
# Set high accuracy mode
depth_sensor = pipelineProfile.get_device().first_depth_sensor() 
depth_sensor.set_option(rs.option.visual_preset, rs.rs400_visual_preset.high_density)
depth_scale = depth_sensor.get_depth_scale()

while True:
    
    #config.config.enable_stream(rs.stream.color, 424, 240, rs.format.bgr8, 30)
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()


    if not depth_frame or not color_frame:
        continue

    color_img = np.asanyarray(color_frame.get_data())
    depth_img = np.asanyarray(depth_frame.get_data())
    color_img1 = color_img.copy()



    
    if out == 0:
        
        profile = depth_frame.get_profile()
        intrinsics = profile.as_video_stream_profile().get_intrinsics()
        depth_profile = frames.get_depth_frame().get_profile().as_video_stream_profile()
        color_profile = frames.get_color_frame().get_profile().as_video_stream_profile()

        extrinsics = depth_profile.get_extrinsics_to(color_profile)
        print(f"extrinsics:\n{extrinsics}")
        # print(f"Rotation: {extrinsics.rotation}")
        print(intrinsics)

    out = 1


    

    
    dist1 = depth_frame.get_distance(xBasic,yBasic)
   


    coordinate_3d1 = rs.rs2_deproject_pixel_to_point(intrinsics, (xBasic,yBasic), dist1)
    cv2.circle(color_img, (xBasic,yBasic), 10, (0,255,0), 2)
    cv2.rectangle(color_img, (xBasic-20, yBasic-20), (xBasic+20, yBasic+20), (255,0,0),2)
    cv2.putText(color_img, f'dist: {dist1:.2f}', 
            (xBasic-100, yBasic+40), cv2.FONT_ITALIC, 0.6, (0,0,255), 2)
    


    dist2 = depth_frame.get_distance(xScissor,yScissor)
    coordinate_3d2 = rs.rs2_deproject_pixel_to_point(intrinsics, (xScissor,yScissor), dist2)
    cv2.circle(color_img, (xScissor,yScissor), 10, (0,255,0), 2)
    cv2.rectangle(color_img, (xScissor-20, yScissor-20), (xScissor+20, yScissor+20), (255,0,0),2)
    cv2.putText(color_img, f' dist: {dist2:.2f}', 
            (xScissor-100, yScissor+40), cv2.FONT_ITALIC, 0.6, (255,0,0), 2)

    cv2.imshow('TCP', color_img)
    #cv2.imwrite('TCP.png', color_img)
    cv2.waitKey(1)
    #cv2.destroyAllWindows()