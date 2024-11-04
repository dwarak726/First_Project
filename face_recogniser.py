import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import csv

# Load known faces from pre-encoded .npy files
def load_known_faces_from_encodings(folder):
    known_face_encodings = []
    known_face_names = []
    
    for filename in os.listdir(folder):
        if filename.endswith(".npy"):
            encoding_path = os.path.join(folder, filename)
            face_encoding = np.load(encoding_path)
            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(filename)[0])
    
    return known_face_encodings, known_face_names

# Path to the folder containing encoded .npy files
encoded_folder = r'encoded_pics'
known_face_encodings, known_face_names = load_known_faces_from_encodings(encoded_folder)

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

# Process every n-th frame for face recognition
process_this_frame = True

# CSV file to log recognized faces
csv_file = 'recognition_log.csv'

# Create the CSV file and write the header if it doesn't exist
if not os.path.isfile(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Date', 'Time'])  # Writing header

while True:  # Run indefinitely until a face is recognized
    ret, frame = cap.read()
    if not ret:
        break

    
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # Quarter size
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    
    face_locations = []
    face_encodings = []
    face_names = []

    # Process only every other frame for speed
    if process_this_frame:
       
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

       
        face_names = []
        status_message = "Not a resident "  # Default message
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the first match (if any)
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                print(f"Recognized: {name} - True")  # Print recognized name and True

                # Get current date and time
                now = datetime.now()
                date = now.strftime("%Y-%m-%d")
                time = now.strftime("%H:%M:%S")
                
                # Log recognized name with date and time to CSV
                with open(csv_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([name, date, time])  # Writing name, date, and time
                    print(f"Logged: {name} recognized on {date} at {time}")

                # Display recognition status on frame
                status_message = f"Recognized: {name} - True"
                
                # Exit after recognizing a face
                cap.release()  # Release the webcam
                cv2.destroyAllWindows()  # Close all OpenCV windows
                exit()  # Exit the program
                
            else:
                status_message = "Not a resident - False"  # Update status message for unknown faces

            face_names.append(name)

    process_this_frame = not process_this_frame  # Alternate frame processing

    # Draw rectangles and names
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

    # Display the recognition status message at the top of the frame
    cv2.putText(frame, status_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Show the video feed
    cv2.imshow('Face Recognition', frame)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()