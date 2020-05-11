'''

register_face.py:
    => Haarcascade detect the face
    => Patient ID from patient_id.py
    => Writes images to MediFace_DB

MediFace:
    => www.gitlab.com
    => Developed by Greg Price
    => Individual Project (CS3IP16)

Guidance from:
    => Mjrovai @ towardsdatascience.com
    => Adrian  @ pyimagesearch.com

'''


import cv2.cv2 as cv2
import numpy as np
import imutils
import patient_id
import training


def registerFace():

    f_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(0)  # launches built-in webcam (0)

    new_patient = patient_id.getUID()    # get patient name and UID
    total = 0

    while True:
        # loop over frames from VideoCapture
        ret, frame = video_capture.read() # returns a tuple, number, if successful returns frame
        frame = imutils.resize(frame, width=600)

        # turns image into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # returns rectangle, where face has been detected
        faces = f_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x,y,w,h) in faces:
            # image, start_point, end_point, color, thickness
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

            total += 1
            path = 'MediFace_DB/' + new_patient + '/'
            # save images in the new patient's directory
            cv2.imwrite(path + str(total) + '.jpg', gray[y:y+h,x:x+w])
            cv2.imshow('Register Face', frame)


        key = cv2.waitKey(1) & 0xFF
        # press 'q' to quit, then close VideoCapture
        if key == ord('q'):
            break
        # take 40 face images, then close VideoCapture
        elif total >= 40:
            break

    # close and clean up VideoCapture
    video_capture.release()
    cv2.destroyAllWindows()

    # --------------------! TESTING !---------------------
    faces, labels = training.trainFacesandLabels()
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(labels))))

