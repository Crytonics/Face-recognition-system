import customtkinter
from tkinter import *
from os import path
from configparser import ConfigParser

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "files", "config.ini"))

def clear_buttons_cam_RGBCamera_Settings(Camera_next_btn_RGBCamera, Camera_prev_btn_RGBCamera, Camera_all_btn_RGBCamera):
    global Camera_next_btn_RGB, Camera_prev_btn_RGB, Camera_all_btn_RGB
    Camera_next_btn_RGB = Camera_next_btn_RGBCamera
    Camera_prev_btn_RGB = Camera_prev_btn_RGBCamera
    Camera_all_btn_RGB = Camera_all_btn_RGBCamera

def clear_buttons_cam_GrayCamera_Settings(Camera_next_btn_GrayCamera, Camera_prev_btn_GrayCamera, Camera_all_btn_GrayCamera):
    global Camera_next_btn_GRAY, Camera_prev_btn_GRAY, Camera_all_btn_GRAY
    Camera_next_btn_GRAY = Camera_next_btn_GrayCamera
    Camera_prev_btn_GRAY = Camera_prev_btn_GrayCamera
    Camera_all_btn_GRAY = Camera_all_btn_GrayCamera

def clear_buttons_cam_RGB_NO_Settings(Camera_next_btn_RGB_NO, Camera_prev_btn_RGB_NO, Camera_all_btn_RGB_NO):
    global Camera_next_btn_RGB_N, Camera_prev_btn_RGB_N, Camera_all_btn_RGB_N
    Camera_next_btn_RGB_N = Camera_next_btn_RGB_NO
    Camera_prev_btn_RGB_N = Camera_prev_btn_RGB_NO
    Camera_all_btn_RGB_N = Camera_all_btn_RGB_NO

def clear_buttons_cam_GRAY_NO_Settings(Camera_next_btn_GRAY_NO, Camera_prev_btn_GRAY_NO, Camera_all_btn_GRAY_NO):
    global Camera_next_btn_GRAY_N, Camera_prev_btn_GRAY_N, Camera_all_btn_GRAY_N
    Camera_next_btn_GRAY_N = Camera_next_btn_GRAY_NO
    Camera_prev_btn_GRAY_N = Camera_prev_btn_GRAY_NO
    Camera_all_btn_GRAY_N = Camera_all_btn_GRAY_NO

def spremi_postavke(global_odabir_dvorana):
    parser = ConfigParser()
    parser.read(filepath)

    parser.set('dvorane', 'dvorana', global_odabir_dvorana)
    print("Dvorana: ", global_odabir_dvorana)
    with open (filepath, W) as configfile:
        parser.write(configfile)


def combobox_callback(odabir_dvorana):
        global global_odabir_dvorana

        if odabir_dvorana == "Dvorana 2":
             global_odabir_dvorana = "2"
        if odabir_dvorana == "Dvorana 303":
             global_odabir_dvorana = "303"
        if odabir_dvorana == "Dvorana 309":
             global_odabir_dvorana = "309"
        if odabir_dvorana == "Dvorana 311":
             global_odabir_dvorana = "311"
        if odabir_dvorana == "Dvorana 312":
             global_odabir_dvorana = "312"

        print("combobox dropdown clicked:", odabir_dvorana)
        print("combobox dropdown converted:", global_odabir_dvorana)

def Settings_Page(Right_frame, switch_event, switch_RectangleCamera_event, MainWindow_btn, Data_btn, Settings_btn, stop_thread):
    Settings_frame = customtkinter.CTkFrame(Right_frame, width=1480, height=900)
    Settings_frame.place(x=10, y=0)


    CameraOptions_Label = customtkinter.CTkLabel(Settings_frame, text='Kamera opcije', font=('Bold', 30))
    CameraOptions_Label.place(x=50, y=20)

    Zapis_dvorane_label = customtkinter.CTkLabel(Settings_frame, text='Zapisivanje u bazu opcije', font=('Bold', 30))
    Zapis_dvorane_label.place(x=50, y=300)


    Text_RgbGrayCamera = customtkinter.CTkLabel(Settings_frame, text='Kamera u RGB modu (ON), kamera u GRAY modu (OFF)', font=('normal', 14))
    Text_RgbGrayCamera.place(x=50, y=100)


    Text_RgbGrayCameraRectangle= customtkinter.CTkLabel(Settings_frame, text='Pokaži oznake na kameri (lica)', font=('normal', 14))
    Text_RgbGrayCameraRectangle.place(x=50, y=200)

    odabir_dvorana_label = customtkinter.CTkLabel(Settings_frame, text='Dvorana: ', font=('normal', 14))
    odabir_dvorana_label.place(x=50, y=400)

    parser = ConfigParser()
    parser.read(filepath)
    saved_is_on_off = parser.get('switch', 'is_on')
    saved_is_on_off_RectangleCamera= parser.get('switchRectangleCamera', 'is_on_off_RectangleCamera')
    

    global is_on
    is_on_start = parser.get('switch', 'is_on_start')
    saved_is_True_False_RectangleCamera = parser.get('switchRectangleCamera', 'is_True_False_RectangleCamera')  
    is_on = is_on_start
    is_on_Rectangle =  saved_is_True_False_RectangleCamera
    print ("DATA: ", is_on)
    print ("DATA2: ", is_on_Rectangle)
    if is_on == 'True':
        if is_on_Rectangle == 'True':
            print("GASI RGB")
            global Camera_next_btn_RGB, Camera_prev_btn_RGB, Camera_all_btn_RGB
            Camera_next_btn_RGB.destroy()
            Camera_prev_btn_RGB.destroy()
            Camera_all_btn_RGB.destroy()
        else:
            global Camera_next_btn_RGB_N, Camera_prev_btn_RGB_N, Camera_all_btn_RGB_N
            print("GASI RGB_NO")
            Camera_next_btn_RGB_N.destroy()
            Camera_prev_btn_RGB_N.destroy()
            Camera_all_btn_RGB_N.destroy()
    else:
        if is_on_Rectangle == 'True':
            print("GASI GRAY")
            global Camera_next_btn_GRAY, Camera_prev_btn_GRAY, Camera_all_btn_GRAY
            Camera_next_btn_GRAY.destroy()
            Camera_prev_btn_GRAY.destroy()
            Camera_all_btn_GRAY.destroy()
        else:
            global Camera_next_btn_GRAY_N, Camera_prev_btn_GRAY_N, Camera_all_btn_GRAY_N
            print("GASI GRAY_NO")
            Camera_next_btn_GRAY_N.destroy()
            Camera_prev_btn_GRAY_N.destroy()
            Camera_all_btn_GRAY_N.destroy()

    RgbGrayCamera_Var = customtkinter.StringVar(value=saved_is_on_off)
    RgbGrayCamera = customtkinter.CTkSwitch(master=Settings_frame, text="", command=switch_event,
                                    variable=RgbGrayCamera_Var ,onvalue="on", offvalue="off", switch_width=100, switch_height=10)
    print('saved_is_on_off: ', saved_is_on_off)
    print('switch_var: ', RgbGrayCamera_Var)
    RgbGrayCamera.place(x=450, y=100)

    RectangleCamera_Var = customtkinter.StringVar(value=saved_is_on_off_RectangleCamera)
    RectangleCamera = customtkinter.CTkSwitch(master=Settings_frame, text="", command=switch_RectangleCamera_event,
                                    variable=RectangleCamera_Var ,onvalue="on", offvalue="off", switch_width=100, switch_height=10)
    print('saved_is_on_off_RectangleCamera: ', saved_is_on_off_RectangleCamera)
    print('RectangleCamera_Var: ', RectangleCamera_Var)
    RectangleCamera.place(x=450, y=200)

    parser = ConfigParser()
    parser.read(filepath)
    
    dvorane_config_read = parser.get('dvorane', 'dvorana')


    combobox = customtkinter.CTkComboBox(Settings_frame, values=["Dvorana 2", "Dvorana 303", "Dvorana 309", "Dvorana 311", "Dvorana 312"],
                                        state = "readonly", command=combobox_callback)

    if dvorane_config_read == "2":
        combobox.set("Dvorana 2")
        combobox_var = "Dvorana 2"
    if dvorane_config_read == "303":
        combobox.set("Dvorana 303")
        combobox_var = "Dvorana 303"
    if dvorane_config_read == "309":
        combobox.set("Dvorana 309")
        combobox_var = "Dvorana 309"
    if dvorane_config_read == "311":
        combobox.set("Dvorana 311")
        combobox_var = "Dvorana 311"
    if dvorane_config_read == "312":
        combobox.set("Dvorana 312")
        combobox_var = "Dvorana 312"

    combobox.place(x=250, y=400)
    combobox_callback(combobox_var)

    spremanje_postavki_btn = customtkinter.CTkButton(Settings_frame, text='Spremi', font=('Bold', 17), width=150, height=40,  fg_color='#2B719E', command=lambda: spremi_postavke(global_odabir_dvorana)) # command=lambda: indicate(MainWindow_btn_page)
    spremanje_postavki_btn.place(x=550, y=675)

    MainWindow_btn.configure(state='normal')
    Data_btn.configure(state='normal')
    Settings_btn.configure(state='disabled')