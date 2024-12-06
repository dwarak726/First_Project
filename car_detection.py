import cv2
import numpy as np


# Load YOLO pre-trained model and configuration
def load_yolo_model():
    # Load YOLO model files (these can be downloaded from the YOLO website or other sources)
    yolo_net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")  # Path to YOLO weights and config
    layer_names = yolo_net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in yolo_net.getUnconnectedOutLayers()]
    return yolo_net, output_layers

# Detect vehicles in the image
def detect_vehicle(image):
    # Load the image
    height, width, channels = image.shape
    yolo_net, output_layers = load_yolo_model()

    # Prepare image for YOLO (scaling, normalization, etc.)
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    
    # Perform detection
    yolo_net.setInput(blob)
    outputs = yolo_net.forward(output_layers)

    # Vehicle detection flags
    vehicle_detected = False
    for out in outputs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Check for vehicles: car (2), motorbike (3), bicycle (1), truck (7)
            if confidence > 0.5 and class_id in [1, 2, 3, 7]:  # 1 = bicycle, 2 = car, 3 = motorbike, 7 = truck
                vehicle_detected = True
                break

    return vehicle_detected
