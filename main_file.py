import cv2
import face_recognition
import numpy as np
from datetime import datetime
import csv
from paddleocr import PaddleOCR
import os


#importing function file of vehicle detection:
import car_detection as car_d

#importing function file of character recognisation:
import Character_recognision as cr

#importing function file of character recognisation:
import face_recogniser as fr

def core_capture_process(number_plate_file, log_file):
    cap = cv2.VideoCapture(0)
    numbrplatefound = False
    door=False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Process the captured frame
        door = False
        if car_d.detect_vehicle(frame):
            door = cr.process_frame(frame, number_plate_file, log_file)
        if not door:
            door=fr.main(cap)
        # Print the door status
        print("Now Door is ", door)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

    # Release video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()
# Initialize the OCR model for number plate recognition
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# File paths
number_plate_file = r'vehicle_numberplates.csv'
log_file = r'logs.csv'
core_capture_process(number_plate_file, log_file)