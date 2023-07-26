import customtkinter
from tkinter import *
import cv2
from PIL import Image
import threading
from os import path
import pickle
import time
from skimage.metrics import structural_similarity as ssim
import os
import sys

basepath = path.dirname(__file__)
filepath_labels = path.abspath(path.join(basepath, "..", "files", "labels.pickle"))
filepath_trainner_frontalface = path.abspath(path.join(basepath, "..", "files", "trainner.yml"))
photosPath = path.abspath(path.join(basepath, "..", "files", "UknowFaces"))

Path_connectors = os.path.abspath("connectors")
sys.path.append(Path_connectors)

global all_frame1_set, all_frame2_set
all_frame1_set = 0
all_frame2_set = 0

def all_cameras():
        Camera_all_btn.configure(state='disabled')
        Camera_next_btn.configure(state='normal')
        Camera_prev_btn.configure(state='normal')

        global all_frame1, all_frame2, all_frame1_set, all_frame2_set

        all_frame1_set = 1
        all_frame2_set = 1

        all_frame1 = customtkinter.CTkFrame(R_F, width=679, height=735)
        all_frame1.pack_propagate(False)
        all_frame1.place(x=10, y=0)

        all_frame2 = customtkinter.CTkFrame(R_F, width=679, height=735)
        all_frame2.pack_propagate(False)
        all_frame2.place(x=699, y=0)

        Label_Image = customtkinter.CTkLabel(all_frame1, text='')
        Label_Image2 = customtkinter.CTkLabel(all_frame2, text='')

        lables = {}
        lables2 = {}
        with open(filepath_labels, "rb") as f:
                og_labels = pickle.load(f)
                lables = {v:k for k, v in og_labels.items()}
                lables2 = {v:k for k, v in og_labels.items()}

        def update_frame():
                global faces_detected_frontalface, gray_img, test_img, face_recognizer_frontalface, global_faces_detected_frontalface2, gray_img2, test_img2

                for face in faces_detected_frontalface:
                        (x, y, w, h) = face
                        rol_gray = gray_img[y:y+h, x:x+h]
                        label, confidence = face_recognizer_frontalface.predict(rol_gray)
                        draw_rect(gray_img, face)
                        predict_name = lables[label]

                        if confidence < 85:
                                put_text(gray_img, predict_name, x, y)

                        else:
                                if len(faces_detected_frontalface) > 0:
                                        for (x, y, w, h) in faces_detected_frontalface:
                                                face = test_img[y:y+h, x:x+w]
                                                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                                                face = cv2.resize(face, (256, 256))
                                                put_text(gray_img, "Nepoznato lice", x, y)

                for face2 in global_faces_detected_frontalface2:
                        (x, y, w, h) = face2
                        rol_gray2 = gray_img2[y:y+h, x:x+h]
                        label2, confidence2 = face_recognizer_frontalface.predict(rol_gray2)
                        draw_rect2(gray_img2, face2)
                        predict_name2 = lables2[label2]

                        if confidence2 < 85:
                                put_text2(gray_img2, predict_name2, x, y)

                        else:
                                if len(global_faces_detected_frontalface2) > 0:
                                        for (x, y, w, h) in global_faces_detected_frontalface2:
                                                face2 = test_img2[y:y+h, x:x+w]
                                                face2 = cv2.cvtColor(face2, cv2.COLOR_BGR2GRAY)
                                                face2 = cv2.resize(face2, (256, 256))
                                                put_text(gray_img2, "Nepoznato lice", x, y)

                video1_pil = Image.fromarray(gray_img)
                video1_tk = customtkinter.CTkImage(video1_pil, size=(735, 735))

                video1_pil2 = Image.fromarray(gray_img2)
                video1_tk2 = customtkinter.CTkImage(video1_pil2, size=(735, 735))

                Label_Image.configure(image=video1_tk)
                Label_Image.pack()
                Label_Image.update()

                Label_Image2.configure(image=video1_tk2)
                Label_Image2.pack()
                Label_Image2.update()

                if not S_T.is_set():
                        Label_Image.after(0, update_frame)
                        #Label_Image2.after(0, update_frame)
        
        thread = threading.Thread(target=update_frame)
        thread.start()

def opencv_GrayCamera(test1, test2, test3, test4, test5, test6, test7):
      global faces_detected_frontalface, gray_img, test_img, face_recognizer_frontalface, global_faces_detected_frontalface2, gray_img2, test_img2
      faces_detected_frontalface = test1
      gray_img = test2
      test_img = test3
      face_recognizer_frontalface = test4
      global_faces_detected_frontalface2 = test5
      gray_img2 = test6
      test_img2 = test7

def draw_rect(test_img,face):
        (x,y,w,h)=face
        cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=2)

def draw_rect2(test_img2,face2):
        (x,y,w,h)=face2
        cv2.rectangle(test_img2,(x,y),(x+w,y+h),(255,0,0),thickness=2)

def put_text(test_img,text,x,y):
        cv2.putText(test_img,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

def put_text2(test_img2,text2,x,y):
        cv2.putText(test_img2,text2,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

def Gray_Camera(stop_thread, MainWindow_btn, Data_btn, Settings_btn, Right_frame, Main_frame, root): 
    global last_saved_time
    time_interval = 3
    last_saved_time = time.time() - time_interval
    
    global root_main
    root_main = root

    global current_person
    current_person = 0

    stop_thread.clear()

    MainWindow_btn.configure(state='disabled')
    Data_btn.configure(state='normal')
    Settings_btn.configure(state='normal')

    global Camera_next_btn, Camera_prev_btn, Camera_all_btn
    Camera_next_btn = customtkinter.CTkButton(Main_frame, text='Sljedeća kamera', font=('Bold', 17), width=150, height=50, fg_color='#243782', corner_radius=0, command = lambda: indicate(Camera_option_next_btn)) #command=lambda: indicate(Settings_btn_page)
    Camera_next_btn.place(x=0, y=600)

    Camera_prev_btn = customtkinter.CTkButton(Main_frame, text='Prijašnja kamera', font=('Bold', 17), width=150, height=50, fg_color='#2B719E', corner_radius=0, command = lambda: indicate(Camera_option_prev_btn)) #command=lambda: indicate(Settings_btn_page)
    Camera_prev_btn.place(x=0, y=650)

    Camera_all_btn = customtkinter.CTkButton(Main_frame, text='Sve kamere', font=('Bold', 17), width=150, height=50, fg_color='#243782', corner_radius=0, command = lambda: indicate(all_cameras)) #command=lambda: indicate(Settings_btn_page)
    Camera_all_btn.place(x=0, y=710)

    thread = None
    global R_F, S_T
    R_F = Right_frame
    S_T = stop_thread

    from Data import clear_buttons_cam_GrayCamera
    clear_buttons_cam_GrayCamera(Camera_next_btn, Camera_prev_btn, Camera_all_btn)

    from Settings import clear_buttons_cam_GrayCamera_Settings
    clear_buttons_cam_GrayCamera_Settings(Camera_next_btn, Camera_prev_btn, Camera_all_btn)

    Camera_option_next_btn()

def indicate(page):
    delete_pages()
    page()

def delete_pages():
    if all_frame1_set == 1:
        for frame in all_frame1.winfo_children():
                frame.destroy()

    if all_frame2_set == 1:
        for frame in all_frame2.winfo_children():
                frame.destroy()

    for frame in R_F.winfo_children():
        frame.destroy()

def Camera_option_next_btn():
        global all_frame1_set, all_frame2_set
        all_frame1_set = 0
        all_frame2_set = 0

        global Camera_next_btn
        Camera_next_btn.configure(state='disabled')
        Camera_prev_btn.configure(state='normal')
        Camera_all_btn.configure(state='normal')

        Label_Image = customtkinter.CTkLabel(R_F, text='')

        lables = {}
        lables2 = {}
        with open(filepath_labels, "rb") as f:
                og_labels = pickle.load(f)
                lables = {v:k for k, v in og_labels.items()}
                lables2 = {v:k for k, v in og_labels.items()}

        def update_frame():
                global faces_detected_frontalface, gray_img, test_img, face_recognizer_frontalface, global_faces_detected_frontalface2, gray_img2, test_img2

                for face in faces_detected_frontalface:
                        (x, y, w, h) = face
                        rol_gray = gray_img[y:y+h, x:x+h]
                        label, confidence = face_recognizer_frontalface.predict(rol_gray)
                        draw_rect(gray_img, face)
                        predict_name = lables[label]

                        if confidence < 85:
                                put_text(gray_img, predict_name, x, y)

                        else:
                                if len(faces_detected_frontalface) > 0:
                                        for (x, y, w, h) in faces_detected_frontalface:
                                                face = test_img[y:y+h, x:x+w]
                                                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                                                face = cv2.resize(face, (256, 256))
                                                put_text(gray_img, "Nepoznato lice", x, y)

                video1_pil = Image.fromarray(gray_img)
                video1_tk = customtkinter.CTkImage(video1_pil, size=(1500, 1000))

                Label_Image.configure(image=video1_tk)
                Label_Image.pack()
                Label_Image.update()

                if not S_T.is_set():
                        Label_Image.after(0, update_frame)
        
        thread = threading.Thread(target=update_frame)
        thread.start()

def Camera_option_prev_btn():
        global all_frame1_set, all_frame2_set
        all_frame1_set = 0
        all_frame2_set = 0

        global Camera_prev_btn
        Camera_prev_btn.configure(state='disabled')
        Camera_next_btn.configure(state='normal')
        Camera_all_btn.configure(state='normal')

        Label_Image = customtkinter.CTkLabel(R_F, text='')

        lables = {}
        lables2 = {}
        with open(filepath_labels, "rb") as f:
                og_labels = pickle.load(f)
                lables = {v:k for k, v in og_labels.items()}
                lables2 = {v:k for k, v in og_labels.items()}

        def update_frame():
                global faces_detected_frontalface, gray_img, test_img, face_recognizer_frontalface, global_faces_detected_frontalface2, gray_img2, test_img2

                for face2 in global_faces_detected_frontalface2:
                        (x, y, w, h) = face2
                        rol_gray2 = gray_img2[y:y+h, x:x+h]
                        label2, confidence2 = face_recognizer_frontalface.predict(rol_gray2)
                        draw_rect2(gray_img2, face2)
                        predict_name2 = lables2[label2]

                        if confidence2 < 85:
                                put_text2(gray_img2, predict_name2, x, y)

                        else:
                                if len(global_faces_detected_frontalface2) > 0:
                                        for (x, y, w, h) in global_faces_detected_frontalface2:
                                                face2 = test_img2[y:y+h, x:x+w]
                                                face2 = cv2.cvtColor(face2, cv2.COLOR_BGR2GRAY)
                                                face2 = cv2.resize(face2, (256, 256))
                                                put_text(gray_img2, "Nepoznato lice", x, y)

                video1_pil = Image.fromarray(gray_img2)
                video1_tk = customtkinter.CTkImage(video1_pil, size=(1500, 1000))

                Label_Image.configure(image=video1_tk)
                Label_Image.pack()
                Label_Image.update()

                if not S_T.is_set():
                        Label_Image.after(0, update_frame)
        
        thread = threading.Thread(target=update_frame)
        thread.start()