import numpy as np
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
face_cascade = cv2.CascadeClassifier("./lib/haarcascade/haarcascade_frontalface_default.xml")
rightEye_cascade = cv2.CascadeClassifier("./lib/haarcascade/haarcascade_righteye_2splits.xml")
leftEye_cascade = cv2.CascadeClassifier("./lib/haarcascade/haarcascade_lefteye_2splits.xml")
mouth_nose_cascade = cv2.CascadeClassifier("./lib/haarcascade/haarcascade_mcs_mouth_nose.xml")

cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
        rightEye = rightEye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in rightEye:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        leftEye = leftEye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in leftEye:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        mouth_nose = mouth_nose_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in mouth_nose:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()