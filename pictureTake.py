import cv2

img = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = img.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "Photo.png".format(img_counter)
        cv2.imwrite("./images/Photo.png", frame)
        print("{} written!".format(img_name))
        img_counter += 1
        
img.release()

import faceDetect