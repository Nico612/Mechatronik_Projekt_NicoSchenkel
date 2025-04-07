import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics.utils import LOGGER
from ultralytics import YOLO
LOGGER.setLevel(50)  # Setzt das Logging-Level auf CRITICAL, sodass nur kritische Fehler ausgegeben werden.

import time
import csv
import os



def getObjectDimensiont(model,confidence, pipeline, depth_scale, align):
    # Laden des YOLO-Modells
    #model = YOLO("yolov8s.pt")
    #model = YOLO("yolo11n.pt")
    #print(model.model_name, model.version)
    
    
    
    
    # Criteria for bounding boxes
    minConf = confidence                
    maxObjectDistanz = 0.8  # in m  # maybe blur all behind it?
    # minObjectDistanz?
    ignore = ["person"]    

    # Safe size of object every tfreq seconds
    tmeass = 0.25
    tInterval = 2                                                      
    tCompare = time.time()
    i = -1  # index for saving values

    # Arrays für die Bounding Box-Größen                                
    xValues = [-50] * int(tInterval / tmeass)
    yValues = [-50] * int(tInterval / tmeass)
    tolerance = 1  # tolerance of derivating of object size [cm]
    stable_object_detected = False  # Status: Stabil erkannt

    # Array für anzahl an ausgewerteten Pixel zur Dimensionsberechnung
    arraySize =  5 #10

    # Data for Gripper
    dataOfInterest = ['label','xsize', 'ysize', 'distance', 'confidence'  ]
    gripCords = [np.nan, np.nan]
    gripDist = 0
    gripData = [] 



    try:
        end = None  # Variable für das finale Bild mit der roten Bounding Box  

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
            # Getting YOLO predictions
            results = model.predict(color_img, conf=minConf)

            nearest_box = None
            nearest_distance = float('inf')
            nearest_details = None

            if results[0].boxes:
                for result in results[0].boxes:
                    class_id = int(result.cls.item())  
                    class_name = model.names[class_id] 
                    
                    #Filter for non- interrupting  objects
                    if class_name in ignore:
                        continue

                    box = result.xyxy[0].cpu().numpy().astype(int)
                    xmin, ymin, xmax, ymax = box
                    xCenter = (xmin + xmax) // 2
                    yCenter = (ymin + ymax) // 2
                    # Distance to middlepoint of object
                    # gripDist = depth_frame.get_distance((xmin + xmax) // 2, (ymin + ymax) // 2)

                    # Schritt auslagern             
                    profile = depth_frame.get_profile()
                    intrinsics = profile.as_video_stream_profile().get_intrinsics()
                    
                    zArray = np.asanyarray(depth_frame.get_data())
                    z1 = zArray[yCenter - arraySize:yCenter + arraySize, xCenter - arraySize: xCenter + arraySize]
                    z1 = np.median(z1) * depth_scale

                    # das erst nachdem nächstes Objekt identfieziert wude?
                    coordinate_3d1 = rs.rs2_deproject_pixel_to_point(intrinsics, (xmax,ymax), z1)
                    coordinate_3d2 = rs.rs2_deproject_pixel_to_point(intrinsics, (xmin,ymin), z1)

                    x1,y1,z1 = coordinate_3d1
                    x2, y2, z2 = coordinate_3d2

                    xdimension = np.sqrt(abs(x1-x2)**2)*100
                    ydimension = np.sqrt(abs(y1-y2)**2)*100

                        
                    if z1 > 0:
                        mean_depth = z1
                    else:
                        mean_depth = float('inf')           
                        #continue

                    # Get closest object
                    if mean_depth < nearest_distance and mean_depth > 0:            # and mean_depth <= maxObjectDistanz:
                        nearest_distance = mean_depth
                        nearest_box = box
                        nearest_details = {
                            "box": box,
                            "distance": mean_depth,
                            "confidence": result.conf[0].item(),
                            "class_id": int(result.cls.item()),
                        }
                # Filter fo Objects in distance -> check for other methods ( of realsense cam)
                if nearest_details and nearest_details["distance"] <= maxObjectDistanz:
                    box = nearest_details["box"]

                    # Green Box for detected object
                    if not stable_object_detected:
                        color_img1 = color_img.copy()
                        cv2.rectangle(color_img1, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                        label = f"{model.names.get(nearest_details['class_id'], 'Unknown')} {xdimension:.2f}x{ydimension:.2f} ({nearest_details['distance']:.2f} m)"
                        cv2.putText(color_img1, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


                    # Get box size
                    if time.time() - tCompare >= tmeass:
                        tCompare = time.time()
                        
                        i = (i + 1) % len(xValues)
                        yValues[i] = (ydimension)                                    
                        xValues[i] = (xdimension)
                        # print(yValues)
                        # print(xValues)

                        '''
                        änderung gemacht; xmax-xmin -> dimension
                        '''

                        # Check if Object fullfills stability criteria
                        if (max(yValues) - min(yValues)) < tolerance and (max(xValues) - min(xValues)) < tolerance:
                            gripCords = [np.mean(xValues), np.mean(yValues)]
                            gripDist = nearest_details["distance"]


                            # Erstelle ein neues Bild nur mit der roten Bounding Box
                            end = color_img.copy()
                            cv2.imwrite("bild.png", end)
                            cv2.rectangle(end, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
                            cv2.putText(end, f'Object detected! ', (box[0], box[1] - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                            
                            cv2.putText(end, f'Size:  {gripCords[0]:.2f}x{gripCords[1]:.2f}', (box[0], box[3] + 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                            # Programm beenden, da das Objekt stabil erkannt wurde
                            stable_object_detected = True
                            break
                        
            # See what happens by delelting this 
            # Zeige das Bild mit der grünen Bounding Box während der Verarbeitung
            if not stable_object_detected:
                cv2.imshow('Object Detection', color_img1)

            if stable_object_detected:
                break  # Beende die Schleife, wenn das Objekt stabil erkannt wurde

            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:
                break

    finally:


        # Zeige das finale Bild mit der roten Bounding Box
        if end is not None:
            cv2.destroyWindow("Object Detection")
            cv2.imshow('Ready to Grip', end)

            # # Get longest and shortes side of object
            # if gripCords[0]< gripCords[1]:
            #     maxSide = gripCords[1]
            #     minSide = gripCords[0]
            # elif gripCords[1]< gripCords[0]:
            #         maxSide = gripCords[0]
            #         minSide = gripCords[1]
            # else:
            #     maxSide = gripCords[0]      

            
         
        
        

            cv2.waitKey(500)
            print("*******************************************************************************************************************")
            print(f"Object: {model.names[nearest_details['class_id']]}")
            print(f"Bounding Box size: {gripCords[1]:.2f} x {gripCords[0]:.2f}")
            print(f"Distance: {gripDist:.3f}")
            print(f"Confidence: {nearest_details['confidence']:.3f}")
            print("*******************************************************************************************************************")
            print(xValues)
            print(yValues)
            
        else:
            print('No stable object detected.')
        #cv2.destroyAllWindows()



        
    # return  [(obj.values()) for obj in gripData]
    return int(nearest_details['class_id']), (gripCords[1]), (gripCords[0])


    #print(f"Box Size: x: {gripCords[0]}, y:{gripCords[1]} \nDistance to center of object: {gripDist:.3f}")
    
# Objekterkennung
# Objektfilterung
# Objektsatbilität
# Worflow

