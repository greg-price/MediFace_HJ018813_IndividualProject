import recognise_face
import register_face
import pickle
import os


def main():

    # Testing for MediFace
    # Displays Test Menu for Developer to test the ScanFace.py, AddFace.py Recognition


    db_name = 'patients.p'
    db = {}

    # first time you run this, 'patient.p' may not exist
    # so we need to check for its existence before we load
    if os.path.exists(db_name):
        # with statements are very handy for opening files.
        with open(db_name, 'rb') as rfp:
            db = pickle.load(rfp)
        # there's no 'rfp.close()'
        # the "with" clause calls close() automatically

    names = ['gregp', 'mariap', 'stevep']
    uids = ['1564101547', '1419273281', '1379031133']
    total = 0
    for i in names:
        db.update({uids[total] : i})
        total+=1


    '''
    first_name = 'stevep'  # add the patient name here
    uid = '1379031133'  # add their unique id here
    db.update({uid : first_name})
    '''

    # sync the database
    with open(db_name, 'wb') as wfp:
        pickle.dump(db, wfp)

    # re-load the database
    with open(db_name, 'rb') as rfp:
        db = pickle.load(rfp)

    print(db)



    '''
    print('TEST MENU\n'
            '1 = SCAN FACE\n'
            '2 = ADD FACE\n')
    user_option = int(input('Input: '))
    if user_option == 1:
        scan_face.scanFace()
    elif user_option == 2:
        register_face.registerFace()
    '''

if __name__ == '__main__':
    # Enables main to properly run
    main()
