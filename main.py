import subprocess
import tkinter as tk
import os
import datetime
import sys
sys.path.append("c:/users/user/appdata/local/programs/python/python312/lib/site-packages")
import numpy 

import cv2
from PIL import Image, ImageTk
import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray', self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        self.add_webcam(self.webcam_label)
        self.db_dir='db'
        self.log_path="./Log.txt"
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)


    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
            self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        if ret:
            self.most_recent_capture_arr = frame
            img_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self._label.imgtk = imgtk
            self._label.configure(image=imgtk)
            self._label.after(20, self.process_webcam)  # Schedule the next update

    def login(self):
        unknown_img_path = './tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        output = subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]).decode('utf-8')
        name_with_path = output.strip()  # Remove leading/trailing whitespaces
        name = name_with_path.split('\r\n')[0]  # Extract the name from the output
        hello=name.replace("./tmp.jpg,","User:")
        if name in ["unknown_person", "no_persons_found"]:
            util.msg_box("Ups....", "Please register as a new User or try again")
        else:
            util.msg_box("Welcome back", 'Welcome {}.'.format(hello))
            with open(self.log_path, 'a') as f:
                f.write("{} {}\n".format(hello, datetime.datetime.now()))  # Added space between name and timestamp
        os.remove(unknown_img_path)



    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_window)
        accept_button_register_new_user_window.place(x=750, y=300)

        try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, input username:')
        self.text_label_register_new_user.place(x=750, y=70)

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_pil.copy()

    def accept_register_new_window(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        img_np = cv2.cvtColor(numpy.array(self.most_recent_capture_pil), cv2.COLOR_RGB2BGR)
        file_path = os.path.join(self.db_dir, '{}.jpg'.format(name))
        cv2.imwrite(file_path, img_np)
        util.msg_box("Success!","User was register succesfully !")
        self.register_new_user_window.destroy()
        self.main_window.destroy()
    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()
    
    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
