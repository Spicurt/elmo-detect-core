import cv2
from multiprocessing import Process
from subprocess import call
import time
import sys
import random
import numpy
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

def highlightFace(net, video, conf_threshold=0.7):
    videoOpencvDnn=video.copy()
    videoHeight=videoOpencvDnn.shape[0]
    videoWidth=videoOpencvDnn.shape[1]
    blob=cv2.dnn.blobFromImage(videoOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections=net.forward()
    faceBoxes=[]
    for i in range(detections.shape[2]):
        confidence=detections[0,0,i,2]
        if confidence>conf_threshold:
            x1=int(detections[0,0,i,3]*videoWidth)
            y1=int(detections[0,0,i,4]*videoHeight)
            x2=int(detections[0,0,i,5]*videoWidth)
            y2=int(detections[0,0,i,6]*videoHeight)
            faceBoxes.append([x1,y1,x2,y2])
            cv2.rectangle(videoOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(videoHeight/150)), 8)
    return videoOpencvDnn,faceBoxes


parser=argparse.ArgumentParser()
parser.add_argument('--image')

args=parser.parse_args()

faceProto="./Resource/opencv_face_detector.pbtxt"
faceModel="./Resource/opencv_face_detector_uint8.pb"
ageProto="./Resource/age_deploy.prototxt"
ageModel="./Resource/age_net.caffemodel"
genderProto="./Resource/gender_deploy.prototxt"
genderModel="./Resource/gender_net.caffemodel"

MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList=['Male','Female']

faceNet=cv2.dnn.readNet(faceModel,faceProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)

def detection(self):
    import detect
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
                
            resultImg,faceBoxes=highlightFace(faceNet,video)
            if not faceBoxes:
               print("No face detected")

            for faceBox in faceBoxes:
                face=video[max(0,faceBox[1]-padding):
                    min(faceBox[3]+padding,video.shape[0]-1),max(0,faceBox[0]-padding)
                    :min(faceBox[2]+padding, video.shape[1]-1)]

            blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPreds=genderNet.forward()
            gender=genderList[genderPreds[0].argmax()]
            ageNet.setInput(blob)
            agePreds=ageNet.forward()
            age=ageList[agePreds[0].argmax()]
            cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100,0,0), 2, cv2.LINE_AA)
            cv2.imshow("Detecting age and gender", resultImg)
                    
            if cv2.waitKey(0):
                break