import customtkinter
from tkinter import *
import cv2
from PIL import Image
import threading
from os import path
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

        def update_frame():
                global test_img, test_img2

                RGB_image= cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
                video1_pil = Image.fromarray(RGB_image)
                video1_tk = customtkinter.CTkImage(video1_pil, size=(735, 735))

                RGB_image2= cv2.cvtColor(test_img2, cv2.COLOR_BGR2RGB)
                video1_pil2 = Image.fromarray(RGB_image2)
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

def opencv_RGBCameraNoRectanglesLabels(test1, test2):
      global test_img, test_img2
      test_img = test1
      test_img2 = test2

def RGB_Camera_No_Rectangles_Labels(stop_thread, MainWindow_btn, Data_btn, Settings_btn, Right_frame, Main_frame, root): 
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

    from Data import clear_buttons_cam_RGB_NO
    clear_buttons_cam_RGB_NO(Camera_next_btn, Camera_prev_btn, Camera_all_btn)

    from Settings import clear_buttons_cam_RGB_NO_Settings
    clear_buttons_cam_RGB_NO_Settings(Camera_next_btn, Camera_prev_btn, Camera_all_btn)

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

        def update_frame():
                global test_img, test_img2

                RGB_image= cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
                video1_pil = Image.fromarray(RGB_image)
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

        def update_frame():
                global test_img, test_img2

                RGB_image= cv2.cvtColor(test_img2, cv2.COLOR_BGR2RGB)
                video1_pil = Image.fromarray(RGB_image)
                video1_tk = customtkinter.CTkImage(video1_pil, size=(1500, 1000))

                Label_Image.configure(image=video1_tk)
                Label_Image.pack()
                Label_Image.update()

                if not S_T.is_set():
                        Label_Image.after(0, update_frame)
        
        thread = threading.Thread(target=update_frame)
        thread.start()