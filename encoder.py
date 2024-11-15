import face_recognition
import os
import numpy as np

# Path to the folder where the images are stored
image_folder = "containsface"
# Path to save encoded images
encoded_folder = "encoded_pics"

# Create a folder for encoded images if it doesn't exist
if not os.path.exists(encoded_folder):
    os.makedirs(encoded_folder)

# Loop through each image in the folder
for filename in os.listdir(image_folder):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        # Load image
        image_path = os.path.join(image_folder, filename)
        image = face_recognition.load_image_file(image_path)
          
        # Find face encodings (returns a list of encodings for each face in the image)
        face_encodings = face_recognition.face_encodings(image)

        # Save the first encoding, assuming one face per image
        if face_encodings:
            # Save the encoding as a .npy file
            np.save(os.path.join(encoded_folder, f"{os.path.splitext(filename)[0]}.npy"), face_encodings[0])

print("All images have been encoded and saved.")