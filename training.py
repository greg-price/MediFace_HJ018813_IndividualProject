'''

training.py:
    => Loops through images in MediFace_DB
    => LBPH trainer learns the faces
    => Trainer writes to the trainer.yml

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
from PIL import Image
import os


recogniser = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def trainFacesandLabels():
    # iterates through the database of faces & labels and stores the features

    global images, label
    faceList = []
    labelList = []

    for entry in os.scandir('MediFace_DB/'):
        if entry.path.endswith('.', 12, 13):
            os.remove(entry.path)    # removes any directories with '.' e.g '.DS_Store'
        else:
            images = sorted([f for f in os.listdir(entry.path)])
            label = int(entry.name)  # store patient's 10 digit UID to label for recognition in predictFace()

        for image in images:
            path = entry.path + '/' + image
            gray_img = Image.open(path).convert('L')      # stores image as grayscale
            img_numpy = np.array(gray_img, 'uint8')       # unsigned int (0-256) - [x,x,x,x]
            faces = detector.detectMultiScale(img_numpy)  # will detect the faces in the images
            for (x,y,w,h) in faces:
                faceList.append(img_numpy[y:y + h, x:x + w])  # x,y is the starting coordinates
                labelList.append(label)                       # w,h is the width & height of the face

    return faceList, labelList


faces, labels = trainFacesandLabels()
recogniser.train(faces, np.array(labels))  # stores labels inside of an array
recogniser.write('Trainer/trainer.yml')    # saves the model into Trainer/trainer.yml

# --------------------! TESTING !---------------------
# Display's how many faces have been trained
print("{0} faces trained".format(len(np.unique(labels))))

# Display's current directories in 'MediFace_DB'
# print(os.listdir('MediFace_DB/'))

# Display's current Faces from 'MediFace_DB'
# print('dataset(): Faces: ')
# print(faces)

# Display's current Labels in 'MediFace_DB'
# print('dataset(): Labels: ')
# print(labels)
