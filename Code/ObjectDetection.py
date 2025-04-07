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
    
    
    print('start')
    
    # Criteria for bounding boxes
    minConf = confidence     # Tresshold for YOLO           
    maxObjectDistanz = 0.8   # Max Distance for recognized Objects
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
    stable_object_detected = False  

    # Array für anzahl an ausgewerteten Pixel zur Dimensionsberechnung
    arraySize =  5 #10

    # Data for Gripper
    dataOfInterest = ['label','xsize', 'ysize', 'distance', 'confidence'  ]
    gripCords = [np.nan, np.nan]
    gripDist = 0
    gripData = [] 



    try:
        end = None  # Flagge zum Beenden der while Schleife

        while True:
            # Get images
            frames = pipeline.wait_for_frames()
            # Align the depth frame to color frame
            aligned_frames = align.process(frames)

            depth_frame = aligned_frames.get_depth_frame() 
            color_frame = aligned_frames.get_color_frame()
            # Wait for frames
            if not depth_frame or not color_frame:
                continue

            color_img = np.asanyarray(color_frame.get_data())
           
            color_img1 = color_img.copy()
            # Getting YOLO predictions
            results = model.predict(color_img, conf=minConf)

            nearest_box = None
            nearest_distance = float('inf')
            nearest_details = None
            # Analyze all YOLO results
            if results[0].boxes:
                for result in results[0].boxes:
                    class_id = int(result.cls.item())  
                    class_name = model.names[class_id] 
                    
                    #Filter for specified objects
                    if class_name in ignore:
                        continue
                    # Get coordinates
                    box = result.xyxy[0].cpu().numpy().astype(int)
                    xmin, ymin, xmax, ymax = box
                    xCenter = (xmin + xmax) // 2
                    yCenter = (ymin + ymax) // 2

                    # Parameter to calculate depth
                    profile = depth_frame.get_profile()
                    intrinsics = profile.as_video_stream_profile().get_intrinsics()
                    # Analyze specified ROI
                    zArray = np.asanyarray(depth_frame.get_data())
                    z1 = zArray[yCenter - arraySize:yCenter + arraySize, xCenter - arraySize: xCenter + arraySize]
                    z1 = np.median(z1) * depth_scale

                    # Get 3D-Coordinates
                    coordinate_3d1 = rs.rs2_deproject_pixel_to_point(intrinsics, (xmax,ymax), z1)
                    coordinate_3d2 = rs.rs2_deproject_pixel_to_point(intrinsics, (xmin,ymin), z1)

                    x1,y1,z1 = coordinate_3d1
                    x2, y2, z2 = coordinate_3d2
                    # Calculate x and y dimension
                    xdimension = np.sqrt(abs(x1-x2)**2)*100
                    ydimension = np.sqrt(abs(y1-y2)**2)*100

                    # Filter for Objects with relevant Depth
                    if z1 > 0 and z1 <= maxObjectDistanz:
                        mean_depth = z1
                    else:         
                        continue

                    # Get closest object
                    if mean_depth < nearest_distance :            
                        nearest_distance = mean_depth
                        nearest_box = box
                        nearest_details = {
                            "box": box,
                            "distance": mean_depth,
                            "confidence": result.conf[0].item(),
                            "class_id": int(result.cls.item()),
                        }
                # Store Information of closest object
                if nearest_details :
                    box = nearest_details["box"]

                    # Green Box for detected object
                    if not stable_object_detected:
                        color_img1 = color_img.copy()
                        cv2.rectangle(color_img1, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                        label = f"{model.names.get(nearest_details['class_id'], 'Unknown')} {xdimension:.2f}x{ydimension:.2f} ({nearest_details['distance']:.2f} m)"
                        cv2.putText(color_img1, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Stabilitätskriterium
                    if time.time() - tCompare >= tmeass:
                        tCompare = time.time()
                        
                        i = (i + 1) % len(xValues)
                        yValues[i] = (ydimension)                                    
                        xValues[i] = (xdimension)
              
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
            if end is None:              #stable_object_detected:# end
                cv2.imshow('Object Detection', color_img1)

            if end is not None:
                break  # Beende die Schleife, wenn das Objekt stabil erkannt wurde

            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:
                break

    finally:


        # Zeige das finale Bild mit der roten Bounding Box
        if end is not None:
            cv2.destroyWindow("Object Detection")
            cv2.imshow('Ready to Grip', end)


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

    return int(nearest_details['class_id']), (gripCords[1]), (gripCords[0])

