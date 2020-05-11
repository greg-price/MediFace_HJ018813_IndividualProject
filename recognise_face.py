'''

recognise_face.py:
    => Camera launches on Patient
    => Frame is turned into grayscale
    => LBPH predicts Patient from reading trainer.yml

MediFace:
    => www.gitlab.com
    => Developed by Greg Price
    => Individual Project (CS3IP16)

Guidance from:
    => Mjrovai @ towardsdatascience.com
    => Adrian  @ pyimagesearch.com

'''


import cv2.cv2 as cv2
import imutils
import training
import patient_id

training.trainFacesandLabels()
face_recogniser = cv2.face.LBPHFaceRecognizer_create()  # OpenCV face_recogniser via LBPH
face_recogniser.read('Trainer/trainer.yml')  # save the matrices of people's faces


def predictFace(img):
    # predicts the faces and labels
    # draws the rectangle and label around a detected face during the VideoCapture

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert image to gray scale
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  # pre-trained file on + & - images
    faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        # image, start_point, end_point, color, thickness
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,0,0), 2)
        label_prediction, confidence = face_recogniser.predict(gray[y:y + h, x:x + w])

        # when confidence is less than 50, then successful match
        if (confidence < 50):
            confidence = '{0}%'.format(round(100 - confidence))
            label_text = label_prediction
            return img, True, label_prediction
        else:
            label_text = 'unknown'
            confidence = '{0}%'.format(round(100 - confidence))
        cv2.putText(img, label_text, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        # --------------------! TESTING !---------------------
        # Display's the prediction through LBPH from patients faces
        # print('predictFace(): Prediction: ')
        # print(label_prediction)

    return img, False, ''  # if face isn't recognised, then return false


def recogniseFace():
    # opencv VideoCapture with imutils to adapt streaming output for improved detection

    video_capture = cv2.VideoCapture(0)  # launches built-in webcam (approx 30fps)
    while True:
        ret, frame = video_capture.read()  # ret is if successful, frame is an image
        # adjusts size of video frame (reduces confidence rating)
        frame = imutils.resize(frame, width=600)
        frame, proceed, patient = predictFace(frame)
        cv2.imshow('Recognise Face', frame)  # shows VideoCapture in frame

        if proceed is True:
            # patient identified, return to gui to load Medical ID
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # press 'q' to quit and close MediFace
            break

    # close and clean up VideoCapture
    video_capture.release()
    cv2.destroyAllWindows()
    return proceed, patient  # True/ False, Patient ID/''
