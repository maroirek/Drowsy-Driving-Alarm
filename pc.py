import cv2 as cv
from PIL import Image
import os

cap = cv.VideoCapture(0)   
if not cap.isOpened():
    print("Cannot open camera")
    exit()
       
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    im = Image.fromarray(frame)
    im.save("image.jpeg")
    
    os.system('cmd /k "cd se"')
    os.system('cmd /k "scp image.jpeg pi@192.168.137.156:~/"')
    
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()