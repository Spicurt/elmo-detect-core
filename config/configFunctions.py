import cv2
from multiprocessing import Process
from subprocess import call
import time
import sys

img_counter = 0

def detect():
    while True:
        img_e = cv2.imread("./images/Photo.png")
        classifier = cv2.CascadeClassifier('./lib/haarcascade/haarcascade_frontalface_default.xml')
        eye_classifier = cv2.CascadeClassifier('./lib/haarcascade/haarcascade_eye_tree_eyeglasses.xml')

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

        if cv2.waitKey(1):
            break    