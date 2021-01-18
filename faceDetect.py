from cv2 import imread
from cv2 import imshow
from cv2 import waitKey
from cv2 import destroyAllWindows
from cv2 import CascadeClassifier
from cv2 import rectangle
import cv2

k = cv2.waitKey(1)

img = imread('./images/Photo.png')

classifier = CascadeClassifier('./lib/haarcascade/haarcascade_frontalface_default.xml')
eye_classifier = CascadeClassifier('./lib/haarcascade/haarcascade_eye_tree_eyeglasses.xml')

faceBox = classifier.detectMultiScale(img)

for box in faceBox:
    x, y, width, height = box
    x2, y2 = x + width, y + height
    rectangle(img, (x, y), (x2, y2), (0,0,255), 1)

eyeBoxes = eye_classifier.detectMultiScale(img)

for box in eyeBoxes:
    x, y, width, height = box
    x2, y2 = x + width, y + height
    rectangle(img, (x, y), (x2, y2), (0,255,0), 1)

imshow('face detection', img)

if k%256 == 27:
    img:release()

waitKey(0)

destroyAllWindows()

