import cv2
import numpy as np
from time import sleep
# from keras.models import load_model
from statistics import mode

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

# Select default camera and set the size
cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)

# Borders to determine the robot movement
left_border = 240
right_border = 80
face_max = 230
face_min = 180

# The following code is to test on laptop
# cap.set(3,1280)
# cap.set(4,720)
# left_border = 950
# right_border = 420
# face_max = 830
# face_min = 750

# Decide to turn left or right when the user move too fast
turn_left = False
turn_right = False

# note: change to thread
# Flags to decide at what time the robot should move
timer = 5
moveback_flag = 0;
moveforward_flag = 0;
moveleft_flag = 0;
moveright_flag = 0;
no_face_timer = 0
face_in_place_stabiliser = 10;

# Detect the borders
"""def FaceBorder(face_centre):
    if(face_centre > left_border):
        # Rotate robot to left
        print("out of left border")
    if(face_centre < right_border):
        # Rotate robot to right
        print("out of right border")
"""
def resetAllFlags(left, right, forward, backward, reset):
    moveback_flag = 0
    moveforward_flag = 0
    moveleft_flag = 0
    moveright_flag = 0
    return;

while True:
    # sleep(0.2)
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

            # Reset all flags
            moveback_flag = 0
            moveforward_flag = 0
            moveleft_flag = 0
            moveright_flag = 0
            no_face_timer += 1

            # This will decide to turn left or right
            # when the user move too fast
            if(no_face_timer > timer):
                print("Left is %s Right is %s" % (turn_left,turn_right))
                # if(turn_left):
                #     client.publish("topic/motor-A/dt", "2");
                # elif(turn_right):
                #     client.publish("topic/motor-A/dt", "3");
                # else:
                #     client.publish("topic/motor-A/dt", "4");
                no_face_timer = 0

        # draw rectangle on closest face
        if (biggestFace > 0):
            cv2.rectangle(img, (_x,_y), (_x+_w, _y+_h), (255,0,0), 2)
            centre_x = _x + _w/2
            centre_h = _w + _h/2
            # print("centre_x is at: %i"  %centre_x)
            # print("centre_h is: %i" %centre_h)

            no_face_timer = 0

            # check if face is out of the border
            if(centre_h > face_max):
                # move robot back when the user is too close (note: change to threadg)
                moveback_flag+=1
                face_in_place_stabiliser-=1
                if(moveback_flag > timer and face_in_place_stabiliser <= 0):
                    print("face too big")
                    # client.publish("topic/motor-A/dt", "0");
                    moveback_flag = 0

                # Reset other flags
                moveforward_flag = 0
                moveleft_flag = 0
                moveright_flag = 0

            elif(centre_h < face_min):
                # move robot forward when the user is too far (note: change to thread)
                moveforward_flag+=1
                face_in_place_stabiliser-=1
                if(moveforward_flag > timer and face_in_place_stabiliser <= 0):
                    print("face too small")
                    # client.publish("topic/motor-A/dt", "1");
                    moveforward_flag = 0
                    print("face_in_place_stabiliser is: %i"  %face_in_place_stabiliser)

                # Reset other flags
                moveback_flag = 0
                moveleft_flag = 0
                moveright_flag = 0

            else:
                # When the user is within teh distance to interact the robot
                if(centre_x > left_border):
                    # Rotate robot to left when the user moves left (note: change to thread)
                    turn_left = True
                    turn_right = False
                    moveleft_flag+=1
                    face_in_place_stabiliser-=1
                    if(moveleft_flag > timer and face_in_place_stabiliser <= 0):
                        print("out of left border")
                        # client.publish("topic/motor-A/dt", "3");
                        moveleft_flag = 0

                    # Reset other flags
                    moveforward_flag = 0
                    moveback_flag = 0
                    moveright_flag = 0

                elif(centre_x < right_border):
                    # Rotate robot to right when the user moves to the right(note: change to thread)
                    turn_right = True
                    turn_left = False
                    moveright_flag+=1
                    face_in_place_stabiliser-=1
                    if(moveright_flag > timer and face_in_place_stabiliser <= 0):
                        print("out of right border")
                        # client.publish("topic/motor-A/dt", "2");
                        moveright_flag = 0

                    # Reset other flags
                    moveforward_flag = 0
                    moveback_flag = 0
                    moveleft_flag = 0

                else:
                    print("face ok")
                    face_in_place_stabiliser = 10;
                    print("face_in_place_stabiliser is: %i"  %face_in_place_stabiliser)
                    # client.publish("topic/motor-A/dt", "4");

                    # reset turing and all the flags
                    turn_left = False
                    turn_right = False
                    moveback_flag = 0
                    moveforward_flag = 0
                    moveleft_flag = 0
                    moveright_flag = 0


        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

client.disconnect();
cap.release()
cv2.destroyAllWindows()
