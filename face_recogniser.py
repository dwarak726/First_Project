import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import csv

def load_known_faces_from_encodings(folder):
    """Load known face encodings and names from .npy files in a folder."""
    known_face_encodings = []
    known_face_names = []
    
    for filename in os.listdir(folder):
        if filename.endswith(".npy"):
            encoding_path = os.path.join(folder, filename)
            face_encoding = np.load(encoding_path)
            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(filename)[0])
    
    return known_face_encodings, known_face_names



def log_recognition(name, csv_file):
    """Log recognized face information into the CSV file."""
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, time, ' ', name])  # Assuming number plate is not used

def recognize_faces(frame, known_face_encodings, known_face_names):
    """Recognize faces in a given frame."""
    rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            face_names.append(name)
        else:
            face_names.append(name)
    
    return face_locations, face_names

def draw_face_boxes(frame, face_locations, face_names):
    """Draw rectangles around recognized faces in the frame."""
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw the face box
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        # Label with name
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

def main(cap):
    # Load known faces
    encoded_folder = r'encoded_pics'
    known_face_encodings, known_face_names = load_known_faces_from_encodings(encoded_folder)

    # Initialize webcam
    
    # CSV file to log recognized faces
    csv_file = 'logs.csv'
    
    process_this_frame = True

    ret, frame = cap.read()

    if process_this_frame:
        face_locations, face_names = recognize_faces(frame, known_face_encodings, known_face_names)
              
        status_message = ""
        doorstat=False
        for name in face_names:
            if name != "Unknown":
                log_recognition(name, csv_file)
                status_message = f"Recognized: {name} - True"
                doorstat=True
                break  # Stop after logging the first recognized name
        
    process_this_frame = not process_this_frame
        
    # Draw face boxes and display the status message
    draw_face_boxes(frame, face_locations, face_names)
    cv2.putText(frame, status_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Show the video feed
    cv2.imshow('Face Recognition', frame)
    print(status_message)
    
    # Release resources
    return doorstat