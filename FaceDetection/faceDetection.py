import cv2
import numpy as np
import time

face_cascade =cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Don't need
# eye_cascade =cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
left_border = 700
right_border = 500
face_max = 350
face_min = 280

def FaceBorder(x):
    if(x > left_border):
        # Rotate robot to left
        print("out of left border")
    if(x < right_border):
        # Rotate robot to right
        print("out of right border")

while True:
    # Reduce size
    # time.sleep(2)
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 3)
    # first_face = faces[0]
    # print("Found %s faces!" % len(faces))
    # if len(faces) != 0:
    #     print("FACE")
    # else:
    #     print("NO FACE")
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        centre_x = x + w/2
        # centre_y = y + y/2
        # print("X is %i, Y is %i, W is %i, H is %i" % (x, y, w, h))

        # check if face is out of the border
        if(h > face_max):
            # move robot back
            print("face too big")
        elif(h < face_min):
            # move robot forward
            print("face too small")
        else:
            FaceBorder(centre_x)

        # print("h is %i" %(h))
        # roi_gray= gray[y:y+h, x:x+w]
        # roi_color = img[y:y+h, x:x+w]
        # eyes = eye_cascade.detectMultiScale(roi_gray)
        # for(ex,ey,ew,eh) in eyes:
        #     cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+ew), (0,255,0), 2)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
