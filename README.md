# Secure-nest
<div style="display: flex; align-items: center;">
  <img src="https://res.cloudinary.com/dvsxdaexn/image/upload/v1732089516/sec2_evbhu8.jpg" alt="Secure Nest" style="height:100px;width:100px;">
</div>



## Table of Contents
- [Abstract](#Abstract) <br>
- [Requirements](#requirements) <br>
- [How to use](#installation-and-usage) <br>
- [Preview](#previews) <br>
- [Contribution](#contribution)


## Abstract
<p align="left">      Secure Nest is an automated security solution for residential complexes, enhancing safety and streamlining access control. It uses object detection, license plate recognition, and face recognition to ensure secure entry. For vehicles, cameras scan license plates to match registered residents, granting access upon a match. For pedestrians, face recognition verifies identities against stored profiles. This is a dual-portal visitor management system whereby residents preauthorize entry with the use of a one-time password sent to the visitor's mobile. The access is thus made possible through the combination of the one-time password with the flat number. Also, an Arduino Nano controls the servo motor such that rotation opens the gate or unlocks it following successful authentication. The servo automatically returns to its original position to secure the gate after a preset delay, adding a physical layer of security to the automated system.</p>

## Requirements
||
|--|
|[Python](https://www.python.org/downloads/release/python-3127/)|
opencv-python  [4.8.0](https://opencv.org/releases/)
face-recognition  [1.3.0](https://pypi.org/project/face-recognition/)
numpy  [1.24.4](https://numpy.org/install/)
paddleocr  [2.6.1.3](https://github.com/PaddlePaddle/PaddleOCR)
firebase-admin  [6.1.0](https://pypi.org/project/firebase/)





## Installation and usage
- Clone the repository using
  ```
  git clone https://github.com/AAC-Open-Source-Pool/Secure-nest
  ```
- Install all the dependencies using
  ```
  pip install -r requirements.txt
  ```
- Run encoder.py to add your face into the encoded folder
- Now Run main_file.py to see whether it opens up the gate
- now open the websites [Authorisation_website](https://securenest.ccbp.tech/) to allow outside access while [otp check](https://securenest.ccbp.tech/) is used to verify it
  
## Preview
Screenshots of the project
<img src="https://i.imgur.com/ce1a1V5.jpeg">
<img src="https://i.imgur.com/wd5yHi6.png">  

## Contribution 
*This section provides instructions and details on how to submit a contribution via a pull request. It is important to follow these guidelines to make sure your pull request is accepted.*
1. Before choosing to propose changes to this project, it is advisable to go through the readme.md file of the project to get the philosophy and the motive that went behind this project. The pull request should align with the philosophy and the motive of the original poster of this project.
2. To add your changes, make sure that the programming language in which you are proposing the changes should be the same as the programming language that has been used in the project. The versions of the programming language and the libraries(if any) used should also match with the original code.
3. Write a documentation on the changes that you are proposing. The documentation should include the problems you have noticed in the code(if any), the changes you would like to propose, the reason for these changes, and sample test cases. Remember that the topics in the documentation are strictly not limited to the topics aforementioned, but are just an inclusion.
4. Submit a pull request via [Git etiquettes](https://gist.github.com/mikepea/863f63d6e37281e329f8)
