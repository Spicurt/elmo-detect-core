import cv2
from multiprocessing import Process
from subprocess import call
import time
import sys

sys.path.insert(1, './config/')

from configFunctions import detect

img = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def make_1080p():
    img.set(3, 1920)
    img.set(4, 1080)

make_1080p()

font = cv2.FONT_HERSHEY_SIMPLEX

cv2.namedWindow("Picture Take")

img_counter = 0

while True:
    ret, frame = img.read()

    cv2.putText(frame,'Press space to take start.',(50, 50),font, 1,(0, 0, 0),2,cv2.LINE_4) 
    cv2.putText(frame,'Press escape to leave.',(50, 100),font, 1,(0, 0, 0),2,cv2.LINE_4)

    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("Picture Take", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        time.sleep(1)
        sys.exit()
    elif k%256 == 32:
        # SPACE pressed
        k
        img_name = "Photo.png".format(img_counter)
        cv2.imwrite("./images/Photo.png", frame)
        print("{} written!".format(img_name))
        while True:
            img_e = cv2.imread("./images/Photo.png")

            classifier = cv2.CascadeClassifier('./Source/haarcascade_frontalface_alt_tree.xml')
            righteye_classifier = cv2.CascadeClassifier('./Source/haarcascade_righteye_2splits.xml')
            lefteye_classifier = cv2.CascadeClassifier('./Source/haarcascade_lefteye_2splits.xml')

            faceBox = classifier.detectMultiScale(img_e)

            for box in faceBox:
                x, y, width, height = box
                x2, y2 = x + width, y + height
                cv2.rectangle(img_e, (x, y), (x2, y2), (0,0,255), 1)

            ReyeBoxes = righteye_classifier.detectMultiScale(img_e)

            for box in ReyeBoxes:
                x, y, width, height = box
                x2, y2 = x + width, y + height
                cv2.rectangle(img_e, (x, y), (x2, y2), (0,255,0), 1)
                img_counter += 1
                
            LeyeBoxes = lefteye_classifier.detectMultiScale(img_e)

            for box in LeyeBoxes:
                x, y, width, height = box
                x2, y2 = x + width, y + height
                cv2.rectangle(img_e, (x, y), (x2, y2), (0,255,0), 1)
                img_counter += 1

            cv2.imshow('Face Detection', img_e) 

            if cv2.waitKey(1):
                break
        

