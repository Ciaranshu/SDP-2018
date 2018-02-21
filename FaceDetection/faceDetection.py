import cv2
import numpy as np
# from keras.models import load_model
from statistics import mode

face_cascade =cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(1)
left_border = 800
right_border = 460
face_max = 700
face_min = 580
turn_left = False
turn_right = False
# note: change to thread
timer = 5
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
    if ret == True:
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

        # biggestFace value will be 0 if face is not present
        if(biggestFace == 0):
            print("Left is %s Right is %s" % (turn_left,turn_right))
        # draw rectangle on closest face
        if (biggestFace > 0):
            cv2.rectangle(img, (_x,_y), (_x+_w, _y+_h), (255,0,0), 2)
            centre_x = _x + _w/2
            # print("centre_x is at: %i"  %centre_x)

            # check if face is out of the border
            if(_h > face_max):
                # move robot back (note: change to threadg)
                moveforward_flag = 0
                moveback_flag+=1
                if(moveback_flag > timer):
                    print("face too big")
                    moveback_flag = 0
            elif(_h < face_min):
                # move robot forward (note: change to thread)
                moveback_flag = 0
                moveforward_flag+=1
                if(moveforward_flag > timer):
                    print("face too small")
                    moveforward_flag = 0
            else:
                # FaceBorder(centre_x)
                # I'm lazy
                if(centre_x > left_border):
                    # Rotate robot to left (note: change to thread)
                    turn_left = True
                    turn_right = False
                    moveright_flag = 0
                    moveforward_flag = 0
                    moveback_flag = 0
                    moveleft_flag+=1
                    if(moveleft_flag > timer):
                        print("out of left border")
                        moveleft_flag = 0
                elif(centre_x < right_border):
                    # Rotate robot to right (note: change to thread)
                    turn_right = True
                    turn_left = False
                    moveleft_flag = 0
                    moveforward_flag = 0
                    moveback_flag = 0
                    moveright_flag+=1
                    if(moveright_flag > timer):
                        print("out of right border")
                        moveright_flag = 0
                else:
                    print("face ok")
                    # reset turing to false
                    turn_left = False
                    turn_right = False


        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

cap.release()
cv2.destroyAllWindows()
