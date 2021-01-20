import cv2
from multiprocessing import Process
import sys
from subprocess import call

class callPy(object):
    def __init__(self, path = 'faceDetect.py'):
        self.path = path

    def callFile(self):
        call(["Python3", "{}".format(self.path)])

c = callPy()

img = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cv2.namedWindow("Picture Take")

img_counter = 0

while True:
    ret, frame = img.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("Picture Take", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        sys.exit()
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "Photo.png".format(img_counter)
        cv2.imwrite("./images/Photo.png", frame)
        c.callFile()
        print("{} written!".format(img_name))
        img_counter += 1
        sys.exit()
        
img.release()