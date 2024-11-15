from paddleocr import PaddleOCR
import cv2
import datetime
import pandas

# Initialize the OCR model
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Specify language for OCR

def addlog(file_path, text):
    """
    it adds the log to the.
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d , %H:%M:%S")
    with open(file_path, 'a') as file:
        file.write(f"{current_time} , {text} , \n")

def numberplate_registercheck(number_plate_file, text):
    """
    Checks if the recognized text matches any entry in the number plate file.
    """
    with open(number_plate_file, 'r') as file1:
        for file_line in file1:
            if text in file_line:
                return True
    return False

def process_frame(frame, number_plate_file, log_file):
    """
    Perform OCR on the given frame and process the results. 
    Check if the recognized number plate exists in the file and log the results.
    """
    # Perform OCR on the frame
    result = ocr.ocr(frame, cls=True)

    if result is None or len(result) == 0:
        return False  # No text detected, door stays closed

    for line in result:
        if line is not None:
            for word_info in line:
                text = word_info[1][0]  # Extract recognized text

                # Check if the recognized number plate is registered
                if numberplate_registercheck(number_plate_file, text):
                    status_message="numberplate matched"
                    print(f"User {text} with numberplate exists\n")    
                    cv2.putText(frame, status_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    addlog(log_file, text)
                    return True  # Open the door

                print(f"The numberplate '{text}' is not a resident")

    return False  # Door remains closed if no matching number plate is found



# File paths
'''
number_plate_file = r'vehicle_numberplates.csv'
log_file = r'logs.csv'

# Start the video capture and processingq
core_capture_process(number_plate_file, log_file)
'''
