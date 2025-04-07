import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics import YOLO
import time
import csv
import os
from joblib import load


#  mode = 'Basic'

import numpy as np
def get_lowest_nonzero_value(array, depthScale,x,y):
    """Findet den kleinsten Wert in einem NumPy-Array, der ungleich Null ist."""
    nonzero_values = array[array > 0]  # Alle Werte > 0 herausfiltern
    if nonzero_values.size > 0:
        return np.min(nonzero_values) * depthScale # Kleinstes Element zurückgeben
    return 0  # Falls nur Nullen vorhanden sind, None zurückgeben

def closing(pipeline,depthScale,align,mode,x,y):
    #out = 0
    
    #invalid depth for 0.15m
   
    y1 = y
    
    
    xdepth = x

    # Define position of TCPs
    xBasic = 277
    yBasic = 72
    basicRectangleSize = 10

    xScissor = 100
    yScissor = 80
    scissorRectangleSize = 10
    #pipeline.start(config)

    #decFilter =  rs.decimation_filter(2)
    
    
    
    
    
    while True:
        
        #config.config.enable_stream(rs.stream.color, 424, 240, rs.format.bgr8, 30)
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        #decFilter.process(depth_frame)

        if not depth_frame or not color_frame:
            continue

        color_img = np.asanyarray(color_frame.get_data())
        # depth_img = np.asanyarray(depth_frame.get_data())
        # color_img1 = color_img.copy()



        
        # if out == 0:
            
        #     profile = depth_frame.get_profile()
        #     intrinsics = profile.as_video_stream_profile().get_intrinsics()
        #     depth_profile = frames.get_depth_frame().get_profile().as_video_stream_profile()
        #     color_profile = frames.get_color_frame().get_profile().as_video_stream_profile()

        #     extrinsics = depth_profile.get_extrinsics_to(color_profile)
        #     print(f"extrinsics:\n{extrinsics}")
        #     # print(f"Rotation: {extrinsics.rotation}")
        #     print(intrinsics)

        
        zArray = np.asanyarray(depth_frame.get_data())

        # Visualize TCPs
        #cv2.circle(color_img, (xBasic,yBasic), 10, (0,255,0), 2)
        
    #     cv2.putText(color_img, f'TCP: Other Modes', 
    #             (xBasic-100, yBasic+40), cv2.FONT_ITALIC, 0.6, (255,255,255), 2)
        # Scissor
        #cv2.circle(color_img, (xScissor,yScissor), 10, (0,255,0), 2)
        

        cv2.rectangle(color_img, (0, 0), (xdepth, y1), (0, 0, 0), 1)

        
        if mode == 'Scissor':
        
            cv2.rectangle(color_img, (xScissor -scissorRectangleSize, yScissor -scissorRectangleSize), (xScissor+scissorRectangleSize, yScissor+scissorRectangleSize), (255,0,0),2)
            # Get Distance
            
            zScissor = zArray[yScissor-scissorRectangleSize : yScissor+scissorRectangleSize, 
                            xScissor-scissorRectangleSize : xScissor+scissorRectangleSize]
            
            distScissor = np.median(zScissor) * depthScale    # min value = 16
            #distScissor = get_lowest_nonzero_value(zScissor,depthScale)# min value = 15-size = 5


            cv2.putText(color_img, f'dist: {distScissor:.2f}', 
                    (xScissor+0, yScissor+40), cv2.FONT_ITALIC, 0.6, (255,255,255), 2)

            if distScissor < 0.14 and distScissor> 0:
                print('close')
                cv2.destroyAllWindows()
                return True


        else :
            cv2.rectangle(color_img, (xBasic-basicRectangleSize, yBasic-basicRectangleSize), (xBasic+basicRectangleSize, yBasic+basicRectangleSize), (255,0,0),2)
            zBasic = zArray[yBasic-basicRectangleSize : yBasic+basicRectangleSize,
                            xBasic-basicRectangleSize : xBasic+basicRectangleSize]
            distBasic = np.median(zBasic) * depthScale
            
            #distBasic = get_lowest_nonzero_value(zBasic,depthScale)# min value = 15-size = 5
            
            #print(zBasic)
            
            cv2.putText(color_img, f'dist: {distBasic:.2f}', 
                    (xBasic-100, yBasic+40), cv2.FONT_ITALIC, 0.6, (255,255,255), 2)

            if distBasic > 0 and distBasic < 0.14:
                print(closing)
                cv2.destroyAllWindows()
                return True

        # coordinate_3d2 = rs.rs2_deproject_pixel_to_point(intrinsics, (xScissor,yScissor), dist2)
        
        
#or (distScissor < 0.11 and distScissor >0)
        # if (distBasic< 0.11 and distBasic > 0) :
        #     print(distBasic, distScissor)
        #     break
            

        cv2.imshow('TCP', color_img)
        #cv2.imwrite('TCP.png', color_img)
        key = cv2.waitKey(1)
        #cv2.destroyAllWindows()
        if key & 0xFF == ord('q') or key == 27:
            break

cv2.destroyAllWindows()

# config = rs.config()
# config.enable_stream(rs.stream.depth, 424, 240, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  # bgr is compatible with OpenCV
# #pipeline.start(config)
# pipelineProfile = pipeline.start(config)
# # Align Frames to each other
# align_to = rs.stream.color
# align = rs.align(align_to)

# depth_sensor = pipelineProfile.get_device().first_depth_sensor()
# # Set high accuracy mode
# depth_sensor = pipelineProfile.get_device().first_depth_sensor() 
# depth_sensor.set_option(rs.option.visual_preset, rs.rs400_visual_preset.high_accuracy)
# depth_scale = depth_sensor.get_depth_scale()

# x = 424
# y = 240


# dbr = 0.17873
# xdepth = int(dbr * x)
# pipeline = rs.pipeline()
# config = rs.config()
# filter = rs.decimation_filter()
# config.enable_stream(rs.stream.depth, x,y, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, x,y, rs.format.bgr8, 30)  # bgr is compatible with OpenCV 
# pipelineProfile = pipeline.start(config)

# # Align streams
# align_to = rs.stream.color
# align = rs.align(align_to)


# # Set high accuracy mode
# depth_sensor = pipelineProfile.get_device().first_depth_sensor()
# depth_sensor.set_option(rs.option.visual_preset, rs.rs400_visual_preset.high_accuracy)
# #depth_sensor.set_option(rs.option.visual_preset, rs.rs400_visual_preset.medium_density)
# depthScale = depth_sensor.get_depth_scale()
# print(depthScale)


# mode = 'Basic'

# closing(pipeline,depthScale,align,mode,xdepth,y)
# key = cv2.waitKey(1)
