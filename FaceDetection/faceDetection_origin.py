import cv2
import numpy as np
# from keras.models import load_model
# from statistics import mode
#
# import paho.mqtt.client as mqtt
# 0 -goes back forever
# 1 - goes forward forever
# 2 - rotates clockwise forever
# 3 - rotates counterclockwise forever
# 4 - stops any movement

# This is the Publisher
# client = mqtt.Client()
# client.connect("10.42.0.180",1883,60)

face_cascade =cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade =cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
left_border = 950
right_border = 420
face_max = 830
face_min = 750
turn_left = False
turn_right = False
# note: change to thread
timer = 3    # time for the robot to move
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
        # if(biggestFace == 0):
        #     print("Left is %s Right is %s" % (turn_left,turn_right))
            # if(turn_left):
            #     client.publish("topic/motor-A/dt", "2");
            # elif(turn_right):
            #     client.publish("topic/motor-A/dt", "3");
            # else:
            # client.publish("topic/motor-A/dt", "4");
        # draw rectangle on closest face
        if (biggestFace > 0):
            cv2.rectangle(img, (_x,_y), (_x+_w, _y+_h), (255,0,0), 2)
            roi_gray= gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for(ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+ew), (0,255,0), 2)
            centre_x = _x + _w/2
            centre_h = _w + _h/2
            # print("centre_x is at: %i"  %centre_x)
            # print("centre_h is: %i" %centre_h)

            # check if face is out of the border
            if(centre_h > face_max):
                # move robot back (note: change to threadg)
                moveforward_flag = 0
                moveback_flag+=1
                if(moveback_flag > timer):
                    print("face too big")
                    # client.publish("topic/motor-A/dt", "0");
                    moveback_flag = 0
            elif(centre_h < face_min):
                # move robot forward (note: change to thread)
                moveback_flag = 0
                moveforward_flag+=1
                if(moveforward_flag > timer):
                    print("face too small")
                    # client.publish("topic/motor-A/dt", "1");
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
                        # client.publish("topic/motor-A/dt", "3");
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
                        # client.publish("topic/motor-A/dt", "2");
                        moveright_flag = 0
                else:
                    print("face ok")
                    # reset turing to false
                    # client.publish("topic/motor-A/dt", "4");
                    turn_left = False
                    turn_right = False


        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

client.disconnect();
cap.release()
cv2.destroyAllWindows()