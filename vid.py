# Setting up la ras 

import RPi.GPIO as GPIO # known by rasbian to be able to work with GPIO of the ras
GPIO.setmode(GPIO.BOARD)  # to use pin numbers not BCM channel names
buzzer = 12
GPIO.setup(buzzer, GPIO.OUT)   # use pin 12 as output for the buzzer

# Importing libraries
from scipy.spatial import distance
import cv2 as cv
import dlib  
from imutils import face_utils, resize

# calculate the Eye Aspect Ratio  (to determine the state of the eye)
def EAR( eye ) :
    a = distance.euclidean(eye[1], eye[5])
    b = distance.euclidean(eye[2], eye[4])
    c = distance.euclidean(eye[0], eye[3])
    ear = (a + b) / (2.0 * c)
    return ear

Detect_Face = dlib.get_frontal_face_detector()   # select the frontal face detector from dlib
Predict_Landmarks = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") # landmarks detector
lStart, lEnd = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]    # landmarks accorded to left eye 37-42
rStart, rEnd = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]    # landmarks accorded to right eye 43-48  

seuil = 0.20 # we chose it based on the persons distribution

cap = cv.VideoCapture(0)   
if not cap.isOpened():
    print("Cannot open camera")
    exit()
       
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame = resize(frame, width=450)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)   
    faces = Detect_Face(gray, 0)   # we detect faces then we detect landmarks of each face 
    for face in faces :
        shape = Predict_Landmarks(gray,face)
        shape = face_utils.shape_to_np(shape)    # convert to nympy array
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        L_EAR= EAR(leftEye)
        R_EAR= EAR(rightEye)
        Global_EAR = (L_EAR + R_EAR) / 2
        if Global_EAR < seuil :
            GPIO.output(buzzer, GPIO.HIGH)    #kifch y9der ytewel blama ndiro sleep, asynchronous functions python
            d= 1 # 3la l'erreur brk
        else  :
            d= 0 
            GPIO.output(buzzer, GPIO.LOW)  
    
        print(d)
 
    if cv.waitKey(1) == ord('q'):
            break

cap.release()
cv.destroyAllWindows()
GPIO.cleanup()
