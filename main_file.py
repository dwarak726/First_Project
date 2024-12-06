import cv2
import face_recognition
import numpy as np
from paddleocr import PaddleOCR
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
import serial
import time

import car_detection as car_d

import Character_recognision as cr

import face_recogniser as fr

def opendoor(statdoor):
    if statdoor==True:
    # Set up the serial connection
        arduino = serial.Serial(port='COM6', baudrate=115200, timeout=1)  # Replace 'COM5' with your Arduino's port
        time.sleep(2)
        arduino.write(b'1')  # Send the command to rotate the servo
        print("Door has rotated")
        time.sleep(2)        # Wait for the operation to complete
        arduino.close()

def check_visited_status_for_all():
    try:
        ref = db.reference("otp")
        data = ref.get()

        if not data:
            print("No data found in 'otp'.")
            return False

        for key, value in data.items():
            if value.get("visited") == True:
                # Prepare filtered data for 'logs'
                filtered_data = {
                    "flatno": value.get("flatno"),
                    "phone": value.get("phone"),
                    "purpose": value.get("purpose"),
                }

                # Move the filtered data to 'logs'
                logs_ref = db.reference(f"logs/{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                logs_ref.child(key).set(filtered_data)

                # Delete the entry from 'otp'
                ref.child(key).delete()

                print(f"Entry with key {key} has been moved to 'logs' with filtered fields and deleted from 'otp'.")
                return True

        print("No entries with 'visited' set to True.")
        return False

    except Exception as e:
        print(f"Error fetching data: {e}")
        return False


def core_capture_process(number_plate_file):
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        if check_visited_status_for_all():
            print('Outside access has been granted')
        #    opendoor(True)
            continue


        door = False

        # Process the captured frame
        if car_d.detect_vehicle(frame):
            # Call number plate recognition and log to Firebase
            door = cr.process_frame(frame, number_plate_file)
        if not door:
            # Call face recognition and log to Firebase
            door = fr.main(cap)

        # Print the door status
        print("Now Door is ", "Open" if door else "Closed")
        #opendoor(door)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

    # Release video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()
    
# Firebase Initialization
cred = credentials.Certificate(r"C:/Users/dwarak.g/Downloads/project-aac-f5a23-firebase-adminsdk-cjdmf-16dbc41aa2.json")  
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://project-aac-f5a23-default-rtdb.firebaseio.com//' 
})

# Initialize the OCR model for number plate recognition
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# File paths
number_plate_file = r'vehicle_numberplates.csv'  # Path to the number plate file 
# Run the core processing function
core_capture_process(number_plate_file)