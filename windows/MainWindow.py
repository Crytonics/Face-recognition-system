import customtkinter
from tkinter import *
import sys
from os import path
import os
from configparser import ConfigParser
import cv2
import threading
import time

sys.setrecursionlimit(10 ** 9)

Path_Windows = os.path.abspath("windows")
sys.path.append(Path_Windows)

Path_connectors = os.path.abspath("connectors")
sys.path.append(Path_connectors)

from Data import Data_Page
from Settings import Settings_Page
from RGBCamera import RGB_Camera
from GrayCamera import Gray_Camera
from RGBCameraNoRectanglesLabels import RGB_Camera_No_Rectangles_Labels
from GrayCameraNoRectanglesLabels import Gray_Camera_No_Rectangles_Labels

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "files", "config.ini"))
haarcascades_frontalface_path = path.abspath(path.join(basepath, "..", "files", "haarcascades","haarcascade_frontalface_default.xml"))

face_cascade_frontalface = cv2.CascadeClassifier(haarcascades_frontalface_path)

parser = ConfigParser()
parser.read(filepath)
saved_is_on_off = parser.get('switch', 'is_on')
is_on_start = parser.get('switch', 'is_on_start')
saved_is_on_off_RectangleCamera= parser.get('switchRectangleCamera', 'is_on_off_RectangleCamera')
saved_is_True_False_RectangleCamera = parser.get('switchRectangleCamera', 'is_True_False_RectangleCamera')

global stop_thread, is_on

stop_thread = threading.Event()

cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(1 + cv2.CAP_DSHOW)

from opencv import opencv_import
opencv_import(cap, face_cascade_frontalface, stop_thread, cap2) #cap2

is_on = is_on_start

def switch_event():
    global is_on
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "files", "config.ini"))
    parser = ConfigParser()
    parser.read(filepath)
    is_on_start = parser.get('switch', 'is_on_start')  
    is_on = is_on_start 
    if is_on == 'True':
        print("Is off")
        is_on = False
        is_on_False = 'off'
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "..", "files", "config.ini"))
        parser = ConfigParser()
        parser.read(filepath)
        parser.set('switch', 'is_on', is_on_False)
        parser.set('switch', 'is_on_start', str(is_on))
        with open (filepath, W) as configfile:
            parser.write(configfile)
    else:
        print("Is on")
        is_on = True
        is_on_True = 'on'
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "..", "files", "config.ini"))
        parser = ConfigParser()
        parser.read(filepath)
        parser.set('switch', 'is_on', is_on_True)
        parser.set('switch', 'is_on_start', str(is_on))
        with open (filepath, W) as configfile:
            parser.write(configfile)

def switch_RectangleCamera_event():
    global is_on
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "files", "config.ini"))
    parser = ConfigParser()
    parser.read(filepath)
    is_on_start = parser.get('switchRectangleCamera', 'is_True_False_RectangleCamera')  
    is_on = is_on_start 
    if is_on == 'True':
        print("Is off")
        is_on = False
        is_on_False = 'off'
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "..", "files", "config.ini"))
        parser = ConfigParser()
        parser.read(filepath)
        parser.set('switchRectangleCamera', 'is_on_off_RectangleCamera', is_on_False)
        parser.set('switchRectangleCamera', 'is_True_False_RectangleCamera', str(is_on))
        with open (filepath, W) as configfile:
            parser.write(configfile)
    else:
        print("Is on")
        is_on = True
        is_on_True = 'on'
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "..", "files", "config.ini"))
        parser = ConfigParser()
        parser.read(filepath)
        parser.set('switchRectangleCamera', 'is_on_off_RectangleCamera', is_on_True)
        parser.set('switchRectangleCamera', 'is_True_False_RectangleCamera', str(is_on))
        with open (filepath, W) as configfile:
            parser.write(configfile)

def indicate(page):
    delete_pages()
    page()

def close():
    stop_thread.set()
    root.destroy()
    from connector import close_conn
    close_conn()

def MainWindow_btn_page():

    global is_on
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "files", "config.ini"))
    parser = ConfigParser()
    parser.read(filepath)
    is_on_start = parser.get('switch', 'is_on_start')
    saved_is_True_False_RectangleCamera = parser.get('switchRectangleCamera', 'is_True_False_RectangleCamera')  
    is_on = is_on_start
    is_on_Rectangle =  saved_is_True_False_RectangleCamera

    if is_on == 'True':
        if is_on_Rectangle == 'True':
            RGB_Camera(stop_thread, MainWindow_btn, Data_btn, Settings_btn, Right_frame, Main_frame, root) # face_cascade_profileface
        else:
            RGB_Camera_No_Rectangles_Labels(stop_thread, MainWindow_btn, Data_btn, Settings_btn, Right_frame, Main_frame, root)
    else:
        if is_on_Rectangle == 'True':
            Gray_Camera(stop_thread, MainWindow_btn, Data_btn, Settings_btn, Right_frame, Main_frame, root) # face_cascade_profileface
        else:
            Gray_Camera_No_Rectangles_Labels(stop_thread, MainWindow_btn, Data_btn, Settings_btn, Right_frame, Main_frame, root)

def Data_btn_page():
    Data_Page(Right_frame, MainWindow_btn, Data_btn, Settings_btn, stop_thread)

def Settings_btn_page():
    Settings_Page(Right_frame, switch_event, switch_RectangleCamera_event, MainWindow_btn, Data_btn, Settings_btn, stop_thread)

def delete_pages():
    for frame in Right_frame.winfo_children():
        frame.destroy()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title("Sustav prepoznavanja lica")
width_value=root.winfo_screenwidth()
height_value=root.winfo_screenheight()
root.geometry("%dx%d-10+0" % (width_value, height_value-70))

Main_frame = customtkinter.CTkFrame(root, fg_color='#c3c3c3')

Main_frame.pack(side=customtkinter.LEFT)
Main_frame.pack_propagate(False)
Main_frame.configure(width=150, height=1000, fg_color='#282B34')

Right_frame = customtkinter.CTkFrame(root, width=1500, height=1000)
Right_frame.pack_propagate(False)
Right_frame.pack(side=customtkinter.LEFT)

MainWindow_btn = customtkinter.CTkButton(Main_frame, text='Kamera', font=('Bold', 17), width=150, height=50,  fg_color='#2B719E', corner_radius=0, command=lambda: indicate(MainWindow_btn_page))
MainWindow_btn.place(x=0, y=50)

Data_btn = customtkinter.CTkButton(Main_frame, text='Osobe', font=('Bold', 17), width=150, height=50, fg_color='#243782', corner_radius=0, command=lambda: indicate(Data_btn_page))
Data_btn.place(x=0, y=100)

Settings_btn = customtkinter.CTkButton(Main_frame, text='Postavke', font=('Bold', 17), width=150, height=50, fg_color='#2B719E', corner_radius=0, command=lambda: indicate(Settings_btn_page))
Settings_btn.place(x=0, y=149)

time.sleep(0.5)
MainWindow_btn_page()

root.protocol('WM_DELETE_WINDOW', close)
root.mainloop()
