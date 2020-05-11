'''

patient_id.py:
    => Called by gui.py to generate a UID for a new patient
    => Patient ID is created
    => Patient ID and Name is stored in pickle file

MediFace:
    => www.gitlab.com
    => Developed by Greg Price
    => Individual Project (CS3IP16)

Guidance from:
    => Mjrovai @ towardsdatascience.com
    => Adrian  @ pyimagesearch.com

'''


import uuid, pickle
from os import path, makedirs
import os


db = 'patients.p'  # database holding patient id and patient name.

def patientID(f_name, s_name):
    # generate's UID
    # saves the patient's UID and name in pickle file (.p)

    global patient_id
    dataset = {}
    patient_id = str(uuid.uuid4().int >> 64)[:10]  # gen unique 10 digit integer

    # creates/checks new UID -> patient_id doesn't already exist
    if not path.exists('MediFace_DB/' + patient_id):
        makedirs('MediFace_DB/' + patient_id)
    elif path.exists('MediFace_DB/' + patient_id):
        # generates NEW unique 10 digit integer
        patient_id = str(uuid.uuid4().int >> 64)[:10]
        makedirs('MediFace_DB/' + patient_id)

    # creates/checks if patient's medical id doesn't already exist
    if not path.exists('MediFace_ID/' + patient_id + '.txt'):
        os.path.sep.join(['MediFace_ID/' + patient_id + '.txt'])

    # create patient's medical id, copy 'MediFace_ID.txt' file
    with open('MediFace_ID/MediFace_ID.txt') as f:
        with open('MediFace_ID/' + patient_id + '.txt', 'w') as f1:
            for line in f:
                f1.write(line)

    # check for file existence before opening, 'with' will open & close file
    if os.path.exists(db):
        with open(db, 'rb') as rfp:
            dataset = pickle.load(rfp)

    patient_name = f_name + s_name  # gathered from user input in gui.py
    dataset.update({patient_id : patient_name})  # 'key' : 'value'

    # sync and re-load database
    with open(db, 'wb') as wfp:
        pickle.dump(dataset, wfp)
    with open(db, 'rb') as rfp:
        dataset = pickle.load(rfp)

    # --------------------! TESTING !---------------------
    # Display's patient's 10 digit-UID and full name
    # print('PatientID. patient ID: ' + patient_id)
    # print('PatientID. fname: ', f_name)
    # print('PatientID. sname: ', s_name)


def getPatientName(p_id):
    # Loads patient's name from pickle dictionary
    with open(db, "rb") as rf:
        load_id = pickle.load(rf)
    id_name = str(load_id[p_id]) + '_' + str(p_id)  # displays label as '*name*_0123456789'
    return str(id_name)


def getUID():
    # Returns current patient_id for gui.py to access.
    return patient_id
