import cv2
import numpy as np
# from keras.models import load_model
from statistics import mode

face_cascade =cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
left_border = 700
right_border = 500
face_max = 350
face_min = 280
# note: change to thread
moveback_flag = 0;
moveforward_flag = 0;
moveleft_flag = 0;
moveright_flag = 0;

# Detect the borders
"""def FaceBorder(face_centre):
    if(face_centre > left_border):
        # Rotate robot to left
        print("out of left border")
    if(face_centre < right_border):
        # Rotate robot to right
        print("out of right border")
"""

while True:
    biggestFace = 0
    _x = 0
    _y = 0
    _w = 0
    _h = 0
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 3)

    # track the closest face
    for(x,y,w,h) in faces:
        if (w*h > biggestFace):
            _x = x
            _y = y
            _w = w
            _h = h
            biggestFace = _w*_h

    # draw rectangle on closest face
    if (biggestFace > 0):
        cv2.rectangle(img, (_x,_y), (_x+_w, _y+_h), (255,0,0), 2)
        centre_x = _x + _w/2

        # check if face is out of the border
        if(_h > face_max):
            # move robot back (note: change to threadg)
            moveforward_flag = 0
            moveback_flag+=1
            if(moveback_flag > 20):
                print("face too big")
                moveback_flag = 0
        elif(_h < face_min):
            # move robot forward (note: change to thread)
            moveback_flag = 0
            moveforward_flag+=1
            if(moveforward_flag > 20):
                print("face too small")
                moveforward_flag = 0
        else:
            # FaceBorder(centre_x)
            # I'm lazy
            if(centre_x > left_border):
                # Rotate robot to left (note: change to thread)
                moveright_flag = 0
                moveforward_flag = 0
                moveback_flag = 0
                moveleft_flag+=1
                if(moveleft_flag > 20):
                    print("out of left border")
                    moveleft_flag = 0
            if(centre_x < right_border):
                # Rotate robot to right (note: change to thread)
                moveleft_flag = 0
                moveforward_flag = 0
                moveback_flag = 0
                moveright_flag+=1
                if(moveright_flag > 20):
                    print("out of right border")
                    moveright_flag = 0

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
