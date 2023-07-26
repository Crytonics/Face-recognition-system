import customtkinter
import sys
import os
from os import path
from tkinter import *
from configparser import ConfigParser

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "files", "config.ini"))

parser = ConfigParser()
parser.read(filepath)

host=parser.get('database', 'host_set')
database=parser.get('database', 'database_set')
user=parser.get('database', 'user_set')
password=parser.get('database', 'password_set')

path = os.path.abspath("windows")
sys.path.append(path)

def on_entry_click_database_host(event):
    if host_entry.get() == "Host":
        host_entry.delete(0, "end")

def on_focusout_database_host(event):
    if host_entry.get() == '':
        host_entry.insert(0, "Host")

def on_entry_click_database_database(event):
    if database_entry.get() == "Database":
        database_entry.delete(0, "end")

def on_focusout_database_database(event):
    if database_entry.get() == '':
        database_entry.insert(0, "Database")

def on_entry_click_database_user(event):
    if user_entry.get() == "User":
        user_entry.delete(0, "end")

def on_focusout_database_user(event):
    if user_entry.get() == '':
        user_entry.insert(0, "User")

def on_entry_click_database_password(event):
    if password_entry.get() == "Password":
        password_entry.delete(0, "end")
        password_entry.configure(show = '●')

def on_focusout_database_password(event):
    if password_entry.get() == '':
        password_entry.configure(show = '')
        password_entry.insert(0, "Password")
        password_entry.configure(show = '●')

def on_entry_click_login_username(event):
    if entry1.get() == 'Korisnicko ime':
        entry1.delete(0, "end")

def on_focusout_login_username(event):
    if entry1.get() == '':
        entry1.insert(0, 'Korisnicko ime')

def on_entry_click_login_password(event):
    if entry2.get() == 'Lozinka':
        entry2.delete(0, "end")
        entry2.configure(show = '●')

def on_focusout_login_password(event):
    if entry2.get() == '':
        entry2.configure(show = '')
        entry2.insert(0, 'Lozinka')

def login():
    login_connector(root, Username, Password)

def config_database():
    parser = ConfigParser()
    parser.read(filepath)

    host_write = host_entry_load.get()
    database_write = database_entry_load.get()
    user_write = user_entry_load.get()
    password_write = password_entry_load.get()

    parser.set('database', 'host_set', host_write)
    parser.set('database', 'database_set', database_write)
    parser.set('database', 'user_set', user_write)
    parser.set('database', 'password_set', password_write)

    with open (filepath, W) as configfile:
            parser.write(configfile)

    root_database.destroy()
    from connectors.connector import open_conn
    open_conn()

def database_window_login():
    parser = ConfigParser()
    parser.read(filepath)
    
    global host_entry_load, database_entry_load, user_entry_load, password_entry_load, password_entry, host_entry, database_entry, user_entry, root_database
    root_database = customtkinter.CTk()
    root_database.geometry("500x350")

    host_entry_load = customtkinter.StringVar()
    database_entry_load = customtkinter.StringVar()
    user_entry_load = customtkinter.StringVar()
    password_entry_load = customtkinter.StringVar()

    root_database.columnconfigure(0, weight=1)
    root_database.rowconfigure(0, weight=1)

    frame_database = customtkinter.CTkFrame(master=root_database)
    frame_database.grid(row=0, column=0, sticky="nsew")

    frame_database.columnconfigure(0, weight=1)
    frame_database.columnconfigure(1, weight=1)
    frame_database.columnconfigure(2, weight=1)

    label = customtkinter.CTkLabel(master=frame_database, text="Prijava u bazu", font=('Arial', 30, 'bold'), text_color='#1F538D')
    label.grid(row=0, column=0, columnspan=3, pady=20, padx=10)

    host_entry = customtkinter.CTkEntry(master=frame_database, textvariable=host_entry_load)
    host_entry.insert(0, "Host")
    host_entry.bind('<FocusIn>', on_entry_click_database_host)
    host_entry.bind('<FocusOut>', on_focusout_database_host)
    host_entry.grid(row=1, column=0, columnspan=3, pady=12, padx=10, sticky="ew")

    database_entry = customtkinter.CTkEntry(master=frame_database, textvariable=database_entry_load)
    database_entry.insert(0, "Database")
    database_entry.bind('<FocusIn>', on_entry_click_database_database)
    database_entry.bind('<FocusOut>', on_focusout_database_database)
    database_entry.grid(row=2, column=0, columnspan=3, pady=12, padx=10, sticky="ew")

    user_entry = customtkinter.CTkEntry(master=frame_database, textvariable=user_entry_load)
    user_entry.insert(0, "User")
    user_entry.bind('<FocusIn>', on_entry_click_database_user)
    user_entry.bind('<FocusOut>', on_focusout_database_user)
    user_entry.grid(row=3, column=0, columnspan=3, pady=12, padx=10, sticky="ew")

    password_entry = customtkinter.CTkEntry(master=frame_database, textvariable=password_entry_load)
    password_entry.insert(0, "Password")
    password_entry.configure(show = '')
    password_entry.bind('<FocusIn>', on_entry_click_database_password)
    password_entry.bind('<FocusOut>', on_focusout_database_password)
    password_entry.grid(row=4, column=0, columnspan=3, pady=12, padx=10, sticky="ew")

    button = customtkinter.CTkButton(master=frame_database, text="Prijava", command=config_database)
    button.grid(row=5, column=0, columnspan=3, pady=30, padx=10, sticky="ew")

    root_database.mainloop()

if host == 'none' or database == 'none' or user == 'none' or password == 'none':
    database_window_login()

else:
    from connectors.connector import login_connector

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.geometry("500x350")

    global Username
    global Password

    Username = customtkinter.StringVar()
    Password = customtkinter.StringVar()

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    frame = customtkinter.CTkFrame(master=root)
    frame.grid(row=0, column=0, sticky="nsew")


    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)

    label = customtkinter.CTkLabel(master=frame, text="Prijava u sustav", font=('Arial', 30, 'bold'), text_color='#1F538D')
    label.grid(row=0, column=0, columnspan=3, pady=40, padx=10)

    entry1 = customtkinter.CTkEntry(master=frame, textvariable=Username)
    entry1.insert(0, 'Korisnicko ime')
    entry1.bind('<FocusIn>', on_entry_click_login_username)
    entry1.bind('<FocusOut>', on_focusout_login_username)
    entry1.grid(row=1, column=0, columnspan=3, pady=12, padx=10, sticky="ew")

    entry2 = customtkinter.CTkEntry(master=frame, textvariable=Password, show='')
    entry2.insert(0, 'Lozinka')
    entry2.bind('<FocusIn>', on_entry_click_login_password)
    entry2.bind('<FocusOut>', on_focusout_login_password)
    entry2.grid(row=2, column=0, columnspan=3, pady=12, padx=10, sticky="ew")

    button = customtkinter.CTkButton(master=frame, text="Prijava", command=login)
    button.grid(row=3, column=0, columnspan=3, pady=30, padx=10, sticky="ew")

    root.mainloop()

def start_login():
    from connectors.connector import login_connector

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.geometry("500x350")

    global Username
    global Password

    Username = customtkinter.StringVar()
    Password = customtkinter.StringVar()

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    frame = customtkinter.CTkFrame(master=root)
    frame.grid(row=0, column=0, sticky="nsew")

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)

    label = customtkinter.CTkLabel(master=frame, text="Prijava u sustav", font=('Arial', 30, 'bold'), text_color='#1F538D')
    label.grid(row=0, column=0, columnspan=3, pady=40, padx=10)

    entry1 = customtkinter.CTkEntry(master=frame, textvariable=Username)
    entry1.insert(0, 'Korisnicko ime')
    entry1.bind('<FocusIn>', on_entry_click_login_username)
    entry1.bind('<FocusOut>', on_focusout_login_username)
    entry1.grid(row=1, column=0, columnspan=3, pady=12, padx=10, sticky="ew")

    entry2 = customtkinter.CTkEntry(master=frame, textvariable=Password, show='')
    entry2.insert(0, 'Lozinka')
    entry2.bind('<FocusIn>', on_entry_click_login_password)
    entry2.bind('<FocusOut>', on_focusout_login_password)
    entry2.grid(row=2, column=0, columnspan=3, pady=12, padx=10, sticky="ew")

    button = customtkinter.CTkButton(master=frame, text="Prijava", command=login)
    button.grid(row=3, column=0, columnspan=3, pady=30, padx=10, sticky="ew")

    root.mainloop()