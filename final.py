# Importing libraries

import numpy as np
import cv2 as cv 
from PIL import Image

# Cascade Classifier

face_casc = cv.CascadeClassifier('cascades/haarcascade_frontalface_alt2.xml')  # it detects only frontal face
eye_casc = cv.CascadeClassifier('cascades/haarcascade_eye.xml')

# Face detection in a Video Capture

cap = cv.VideoCapture(0)   # 0 for laptop camera
if not cap.isOpened():
    print("Cannot open camera")
    exit()
       
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)   # This kind of cascade classifier works only on gray images
    
    gray1 =  cv.GaussianBlur(gray,(25,25),0)
    ret4,th4 = cv.threshold(gray1,0,255,cv.THRESH_BINARY + cv.THRESH_OTSU)
    
    # faces= face_casc.detectMultiScale(th4, scaleFactor=1.5, minNeighbors=5)
    eyes= eye_casc.detectMultiScale(th4, scaleFactor=1.5, minNeighbors=5)
    
    # for(x,y,w,h) in faces : 
    #     eye=gray[y:y+h, x:x+h]  
    #     eyes= eye_casc.detectMultiScale(eye, scaleFactor=1.5, minNeighbors=5)
    #     for(x1,y1,w1,h1) in eyes : 
    #         cv.rectangle(frame,(x1,y1),(x1+w1, y1+h1), (255,0,0))   # recadrer le visage
    #         cv.imshow('frame', frame)
    
    for(x,y,w,h) in eyes : 
        cv.rectangle(frame,(x,y),(x+w, y+h), (255,0,0))   # recadrer le visage
        cv.imshow('frame', frame)
            
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()