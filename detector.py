import cv2
from multiprocessing import Process
from subprocess import call
import time
import sys
import random
import numpy
import dlib
import math
import argparse
import threading
from playsound import playsound
sys.path.insert(1, './config/')
Sounds = [
            "./Sounds/insult1.wav"
        ]   
from SoundConfig import SoundStart
from SoundConfig import helloElmo
hog_face_detector = dlib.get_frontal_face_detector()

dlib_facelandmark = dlib.shape_predictor("./Resource/shape_predictor_68_face_landmarks.dat")
faceProto = "./Resource/opencv_face_detector.pbtxt"
faceModel = "./Resource/opencv_face_detector_uint8.pb"
ageProto = "./Resource/age_deploy.prototxt"
ageModel = "./Resource/age_net.caffemodel"
genderProto = "./Resource/gender_deploy.prototxt"
genderModel = "./Resource/gender_net.caffemodel"
eyeCascade = cv2.CascadeClassifier("./Resource/haarcascade_eye.xml")
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male','Female']
faceNet = cv2.dnn.readNet(faceModel,faceProto)
ageNet = cv2.dnn.readNet(ageModel,ageProto)
genderNet = cv2.dnn.readNet(genderModel,genderProto)


img = cv2.VideoCapture(0, cv2.CAP_DSHOW)

font = cv2.FONT_HERSHEY_SIMPLEX

play = Process(target = SoundStart)

cv2.namedWindow("Picture Take")

img_counter = 0

hiElmo = Process(target = helloElmo)

hiElmo.start()

#PICTURE TAKE START
while True:
    ret, frame = img.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = hog_face_detector(gray)
    for face in faces:

        face_landmarks = dlib_facelandmark(gray, face)

        for n in range(0, 16):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            cv2.circle(frame, (x, y), 1, (0, 0, 0), 1)

    cv2.putText(frame,'Press space to take start.',(15, 15),font, 0.5,(0, 0, 0),2,cv2.LINE_4) 
    cv2.putText(frame,'Press escape to leave.',(15, 30),font, 0.5,(0, 0, 0),2,cv2.LINE_4)
    cv2.putText(frame,'Press any other key to reload camera.',(15, 45),font, 0.5,(0, 0, 0),2,cv2.LINE_4) 
    """
    eye = eyeCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in eye:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    """
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("Picture Take", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        time.sleep(1)
        exit()
    elif k%256 == 32:
        # SPACE pressed
        k
        img_name = "Photo.png".format(img_counter)
        cv2.imwrite("./images/Photo.png", frame)
        print("{} written!".format(img_name))
        
        playedSound = random.choice(Sounds)

        #Facedetect Loop
        s = Process(target = SoundStart)
        s.start()
        video=cv2.imread('./images/Photo.png')
        padding=20
        while True:
            eyeBox = eyeCascade.detectMultiScale(video)
            for box in eyeBox:
                x, y, width, height = box
                x2, y2 = x + width, y + height
                cv2.rectangle(video, (x,y), (x2,y2), (0,255,0), 1)

            def highlightFace(net, video, conf_threshold=0.7):
                videoOpencvDnn = video.copy()
                videoHeight = videoOpencvDnn.shape[0]
                videoWidth = videoOpencvDnn.shape[1]
                blob = cv2.dnn.blobFromImage(videoOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)
                net.setInput(blob)
                detections = net.forward()
                faceBoxes = []
                eyeBox = []
                for i in range(detections.shape[2]):
                    confidence = detections[0,0,i,2]
                    if confidence > conf_threshold:
                        x1 = int(detections[0,0,i,3] * videoWidth)
                        y1 = int(detections[0,0,i,4] * videoHeight)
                        x2 = int(detections[0,0,i,5] * videoWidth)
                        y2 = int(detections[0,0,i,6] * videoHeight)
                        faceBoxes.append([x1,y1,x2,y2])
                        cv2.rectangle(videoOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(videoHeight/150)), 1)
                
                return videoOpencvDnn,faceBoxes
            video,faceBoxes = highlightFace(faceNet,video)
            if not faceBoxes:
               print("No face detected")
        
            for faceBox in faceBoxes:
                face=video[max(0,faceBox[1] - padding):
                    min(faceBox[3] + padding,video.shape[0] - 1),max(0,faceBox[0] - padding)
                    :min(faceBox[2] + padding, video.shape[1] - 1)]
                
            blob = cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            gender = genderList[genderPreds[0].argmax()]
            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            age = ageList[agePreds[0].argmax()]
            cv2.putText(video, f'{gender}, {age}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2, cv2.LINE_AA)
            cv2.imshow("Detecting age and gender", video)
                    
            if cv2.waitKey(0):
                break
            