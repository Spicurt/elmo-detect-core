import cv2
from multiprocessing import Process
from subprocess import call
import time
import sys
import random
import numpy
from playsound import playsound
sys.path.insert(1, './config/')
Sounds = [
            "./Sounds/insult1.wav"
        ]   
from SoundConfig import SoundStart
from SoundConfig import helloElmo

img = cv2.VideoCapture(0, cv2.CAP_DSHOW)

font = cv2.FONT_HERSHEY_SIMPLEX

play = Process(target = SoundStart)

cv2.namedWindow("Picture Take")

img_counter = 0

hiElmo = Process(target = helloElmo)

hiElmo.start()
while True:
    ret, frame = img.read()

    cv2.putText(frame,'Press space to take start.',(15, 15),font, 0.5,(0, 0, 0),2,cv2.LINE_4) 
    cv2.putText(frame,'Press escape to leave.',(15, 30),font, 0.5,(0, 0, 0),2,cv2.LINE_4)

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
        
        #Facedetect Loop
        
        
        playedSound = random.choice(Sounds)
        
        while True:
            s = Process(target = SoundStart)

            img_e = cv2.imread("./images/Photo.png")

            classifier = cv2.CascadeClassifier('./Resource/haarcascade_frontalface_alt_tree.xml')
            eye_classifier = cv2.CascadeClassifier('./Resource/haarcascade_eye_default.xml')

            faceBox = classifier.detectMultiScale(img_e)

            for box in faceBox:
                x, y, width, height = box
                x2, y2 = x + width, y + height
                cv2.rectangle(img_e, (x, y), (x2, y2), (0,0,255), 1)

            eyeBoxes = eye_classifier.detectMultiScale(img_e)

            for box in eyeBoxes:
                x, y, width, height = box
                x2, y2 = x + width, y + height
                cv2.rectangle(img_e, (x, y), (x2, y2), (0,255,0), 1)
                img_counter += 1

            cv2.imshow('Face Detection', img_e) 

            s.start()
            
            if cv2.waitKey(1):
                break