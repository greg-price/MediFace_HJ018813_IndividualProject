'''

gui.py:
    => MediFaceGUI allows frames to appear in deck style
    => RecogniseFacePage launches recognise_face.py
    => RegisterFacePage launches register_face.py

MediFace:
    => www.gitlab.com
    => Developed by Greg Price
    => Individual Project (CS3IP16)

Guidance from:
    => Mjrovai @ towardsdatascience.com
    => Adrian  @ pyimagesearch.com

'''


from tkinter import *
from tkinter import messagebox
import tkinter as tk
import register_face
import patient_id
import recognise_face


class MediFaceGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)  # frame around the window
        container.pack(side='top', fill='both', expand=True)  # allows expanding of frame via gui
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # store frames in dictionary, load next frame
        for F in (HomePage, RecogniseFacePage, RegisterFacePage):
            frame = F(container, self)  # current frame
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.display_frame(HomePage)  # always show homepage at the start

    def display_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # displays the MediFace logo and underneath the current page
        title_lab = Label(self, text='MediFace', font=('Helvetica 55 bold italic'), fg='#005EB8')
        title_lab.pack(pady=15, padx=0)
        subtitle_lab = Label(self, text='Home Page', font=('Helvetica 14 italic'), fg='#768692')
        subtitle_lab.place(relx=0.5, rely=0.142, anchor=CENTER)

        # launches RecogniseFacePage
        recogniseButton = tk.Button(self, width=20, height=3, text='Recognise Face', font=('Helvetica 13'),
                            command=lambda: controller.display_frame(RecogniseFacePage))
        recogniseButton.place(relx=0.5, rely=0.47, anchor=CENTER)

        # launches RegisterFacePage
        registerButton = tk.Button(self, width=20, height=3, text='Register Face', font=('Helvetica 13'),
                            command=lambda: controller.display_frame(RegisterFacePage))
        registerButton.place(relx=0.5, rely=0.57, anchor=CENTER)


class RecogniseFacePage(tk.Frame):
   def __init__(self, parent, controller):
       tk.Frame.__init__(self, parent)

       # displays the MediFace logo and underneath the current page
       title_lab = Label(self, text='MediFace', font=('Helvetica 55 bold italic'), fg='#005EB8')
       title_lab.pack(pady=15, padx=0)
       subtitle_lab = Label(self, text='Recognise Face', font=('Helvetica 14 italic'), fg='#768692')
       subtitle_lab.place(relx=0.5, rely=0.142, anchor=CENTER)

       # launches recognise_face.py to detect and recognise face
       launchButton = Button(self, width=20, height=3, text='Launch Webcam', font=('Helvetica 13'), command=self.startVideo)
       launchButton.place(relx=0.5, rely=0.5, anchor=CENTER)

       # back button at the bottom of the gui page
       backButton = tk.Button(self, width=10, height=1, text='back', font=('Helvetica 13'),
                              command=lambda: controller.display_frame(HomePage))
       backButton.place(relx=0.5, rely=0.95, anchor=S)


   def startVideo(self):
       verified, pat_id = recognise_face.recogniseFace()  # returns True & Patient's ID, if face has been detected
       if verified is True:
           MediIDPage(pat_id)
           #self.quit()
       #self.quit()


class MediIDPage(tk.Toplevel):
   def __init__(self, p_id):
       tk.Toplevel.__init__(self)
       # Toplevel generates a new window, not part of the frames, but the frames remain open
       self.file_name = str(p_id)
       self.patient_name = patient_id.getPatientName(self.file_name)  # returns 'name_patientid' e.g. gregprice_1231 etc
       self.title(self.patient_name)
       self.geometry('650x650')

       # initilaise the Text() function as self.t, as this will be referenced later
       self.t = Text(self)
       self.t.pack(expand=True, fill='both')
       text = TextWidget(self.t, self.file_name, self.patient_name)

       # creates a pulldown menu, then add it to the menu bar
       menubar = Menu(self)
       filemenu = Menu(menubar, tearoff=0)
       filemenu.add_command(label='Save', command=text.save_file)
       filemenu.add_separator()
       menubar.add_cascade(label='File', menu=filemenu)
       self.config(menu=menubar)

       text.open_file()  # open the MediFace_ID, based on the patient's ID returned


class TextWidget():
    def __init__(self, text, p_id, p_n):

        self.patient_name = p_n
        self.file_name = p_id
        self.text = text

    def open_file(self):
        file = open('MediFace_ID/' + self.file_name + '.txt', 'r+')
        text_value = file.read()
        self.text.delete(1.0, "end-1c")
        self.text.insert("end-1c", text_value)
        file.close()

    def save_file(self):
        file = open('MediFace_ID/' + self.file_name + '.txt', 'w+')
        file.write(self.text.get("1.0", 'end-1c'))
        file.close()


class RegisterFacePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # displays the MediFace logo and underneath the current page
        title_lab = Label(self, text='MediFace', font=('Helvetica 55 bold italic'), fg='#005EB8')
        title_lab.pack(pady=15, padx=0)
        subtitle_lab = Label(self, text='Register Face', font=('Helvetica 14 italic'), fg='#768692')
        subtitle_lab.place(relx=0.5, rely=0.142, anchor=CENTER)

        first_name = Label(self, text='First Name:', font=('Helvetica 13'))
        first_name.place(relx=0.38, rely=0.45, anchor=CENTER)
        last_name = Label(self, text='Last Name:', font=('Helvetica 13'))
        last_name.place(relx=0.38, rely=0.505, anchor=CENTER)

        self.entry_first = Entry(self, width=15)
        self.entry_first.place(relx=0.55, rely=0.45, anchor=CENTER)
        self.entry_last = Entry(self, width=15)
        self.entry_last.place(relx=0.55, rely=0.505, anchor=CENTER)

        proceed = Button(self, width=20, height=3, text='Launch Webcam', font=('Helvetica 13'), command=self.regFace)
        proceed.place(relx=0.5, rely=0.58, anchor=CENTER)

        # back button at the bottom of the gui page
        backButton = tk.Button(self, width=10, height=1, text='back', font=('Helvetica 13'),
                               command=lambda: controller.display_frame(HomePage))
        backButton.place(relx=0.5, rely=0.95, anchor=S)


    def regFace(self):
        f_name = self.entry_first.get()
        l_name = self.entry_last.get()
        patient_id.patientID(f_name, l_name)  # launches pateint_id.py to generate and store a new patient id
        register_face.registerFace()  # launches register_face.py to take 40 greyscale, cropped images
        messagebox.showinfo('Registration Complete', 'New Patient: ' + f_name + ' ' + l_name)
        #self.quit()  # close window


if __name__ == '__main__':
    root = MediFaceGUI()
    root.title('MediFace')
    root.geometry('650x650')
    root.mainloop()
