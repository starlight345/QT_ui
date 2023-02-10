import cv2
for i in range(3):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print("Camera with index {} is working.".format(i))
    else:
        print("Camera with index {} is not working.".format(i))