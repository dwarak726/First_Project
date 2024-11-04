import cv2
import face_recognition
import numpy as np
from datetime import datetime
import csv
from paddleocr import PaddleOCR
import os



#importing function file of character recognisation:
import Character_recognision as cr

# Initialize the OCR model for number plate recognition
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# File paths
number_plate_file = r'vehicle_numberplates.csv'
log_file = r'logs.csv'

cr.core_capture_process(number_plate_file, log_file)