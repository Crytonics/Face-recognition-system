import customtkinter
from tkinter import *
import os
import sys
from tkinter import ttk
from tkinter import filedialog
from configparser import ConfigParser
from os import path

Path_connectors = os.path.abspath("connectors")
sys.path.append(Path_connectors)

def clear_buttons_cam_RGBCamera(Camera_next_btn_RGBCamera, Camera_prev_btn_RGBCamera, Camera_all_btn_RGBCamera):
    global Camera_next_btn_RGB, Camera_prev_btn_RGB, Camera_all_btn_RGB
    Camera_next_btn_RGB = Camera_next_btn_RGBCamera
    Camera_prev_btn_RGB = Camera_prev_btn_RGBCamera
    Camera_all_btn_RGB = Camera_all_btn_RGBCamera

def clear_buttons_cam_GrayCamera(Camera_next_btn_GrayCamera, Camera_prev_btn_GrayCamera, Camera_all_btn_GrayCamera):
    global Camera_next_btn_GRAY, Camera_prev_btn_GRAY, Camera_all_btn_GRAY
    Camera_next_btn_GRAY = Camera_next_btn_GrayCamera
    Camera_prev_btn_GRAY = Camera_prev_btn_GrayCamera
    Camera_all_btn_GRAY = Camera_all_btn_GrayCamera

def clear_buttons_cam_RGB_NO(Camera_next_btn_RGB_NO, Camera_prev_btn_RGB_NO, Camera_all_btn_RGB_NO):
    global Camera_next_btn_RGB_N, Camera_prev_btn_RGB_N, Camera_all_btn_RGB_N
    Camera_next_btn_RGB_N = Camera_next_btn_RGB_NO
    Camera_prev_btn_RGB_N = Camera_prev_btn_RGB_NO
    Camera_all_btn_RGB_N = Camera_all_btn_RGB_NO

def clear_buttons_cam_GRAY_NO(Camera_next_btn_GRAY_NO, Camera_prev_btn_GRAY_NO, Camera_all_btn_GRAY_NO):
    global Camera_next_btn_GRAY_N, Camera_prev_btn_GRAY_N, Camera_all_btn_GRAY_N
    Camera_next_btn_GRAY_N = Camera_next_btn_GRAY_NO
    Camera_prev_btn_GRAY_N = Camera_prev_btn_GRAY_NO
    Camera_all_btn_GRAY_N = Camera_all_btn_GRAY_NO

def Test(one_frame):
            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("dark-blue")

            root_Table = customtkinter.CTk()
            width_value=root_Table.winfo_screenwidth()
            height_value=root_Table.winfo_screenheight()
            root_Table.geometry("%dx%d-10+0" % (width_value, height_value-70))

            style = ttk.Style()

            style.theme_use('default')

            style.configure('Threeview', background = '#D3D3D3', foreground = 'black', rowheight = 25, fieldbackground = '#D3D3D3')

            style.map('Threeview', background = [('selected', '#3f7083')])

            tree_frame = customtkinter.CTkFrame(root_Table)
            tree_frame.pack(pady = 20)

            three_scroll = customtkinter.CTkScrollbar(tree_frame, width = 20)
            three_scroll.pack(side = RIGHT, fill = Y)

            global my_tree
            my_tree = ttk.Treeview(tree_frame, yscrollcommand = three_scroll.set, selectmode = 'extended', height = 25)
            my_tree.pack()

            three_scroll.configure(command = my_tree.yview)

            my_tree ['columns'] = ("Id", "Ime", "Vrijeme")

            my_tree.column("#0", width = 0, stretch = NO)
            my_tree.column("Id", anchor = W, width = 250)
            my_tree.column("Ime", anchor = W, width = 250)
            my_tree.column("Vrijeme", anchor = CENTER, width = 250)

            my_tree.heading("#0", text = "", anchor = W)
            my_tree.heading("Id", text = "Id", anchor = W)
            my_tree.heading("Ime", text = "Ime", anchor = W)
            my_tree.heading("Vrijeme", text = "Vrijeme", anchor = CENTER)

            my_tree.tag_configure('oddrow', background = "white")
            my_tree.tag_configure('evenrow', background = "lightblue")

            data_frame = customtkinter.CTkFrame(root_Table)
            data_frame.pack(fill = 'x', expand = "yes", padx = 20)

            textRecord_data_frame = customtkinter.CTkLabel (data_frame, text = "Podaci", font=('Arial', 23, 'bold'), text_color='#1F538D')
            textRecord_data_frame.grid(row = 0, column = 0, padx = 10, pady = 10)

            Id_Label = customtkinter.CTkLabel(data_frame, text = "Id: ")
            Id_Label.grid(row = 1, column = 0, padx = 10, pady = 10)
            Id_Entry = customtkinter.CTkEntry(data_frame)
            Id_Entry.grid(row = 1, column = 1, padx = 10, pady = 10)

            Ime_Label = customtkinter.CTkLabel(data_frame, text = "Ime: ")
            Ime_Label.grid(row = 1, column = 2, padx = 10, pady = 10)
            Ime_Entry = customtkinter.CTkEntry(data_frame)
            Ime_Entry.grid(row = 1, column = 3, padx = 10, pady = 10)

            Vrijeme_Label = customtkinter.CTkLabel(data_frame, text = "Vrijeme: ")
            Vrijeme_Label.grid(row = 1, column = 4, padx = 10, pady = 10)
            Vrijeme_Entry = customtkinter.CTkEntry(data_frame)
            Vrijeme_Entry.grid(row = 1, column = 5, padx = 10, pady = 10)

            def clear_entries():
                Id_Entry.delete(0, END)
                Ime_Entry.delete(0, END)
                Vrijeme_Entry.delete(0, END)
            
            def remove_one():
                Id_Entry_save = Id_Entry.get()

                from connector import remove_one_data
                remove_one_data(Id_Entry_save)

                x = my_tree.selection()[0]
                my_tree.delete(x)
                Id_Entry.delete(0, END)
                Ime_Entry.delete(0, END)
                Vrijeme_Entry.delete(0, END)

                global messagebox_root
                messagebox_root = customtkinter.CTk()
                messagebox_root.geometry("400x200")

                messagebox_text = customtkinter.CTkLabel(messagebox_root, text = "Uspješno su se izbrisali označeni podaci", font=('Arial', 23, 'bold'), text_color='#1F538D')
                messagebox_text.pack(padx = 10, pady = 20)

                messagebox_button = customtkinter.CTkButton(messagebox_root, text = "Ok", command = messagebox_run)
                messagebox_button.pack(padx = 20, pady = 20)

                messagebox_root.mainloop()

            def messagebox_run():
                messagebox_root.destroy()

            def messagebox_remove_many_ok_run():
                global response
                response = 1
                x = my_tree.selection()
                for record in x:
                    testbroj = my_tree.item(record, 'values')[0]
                    print(testbroj)

                    from connector import remove_many_data
                    remove_many_data(testbroj)

                Id_Entry.delete(0, END)
                Ime_Entry.delete(0, END)
                Vrijeme_Entry.delete(0, END)

                for record in x:
                    my_tree.delete(record)
                messagebox_remove_many_root.destroy()

            def messagebox_remove_many_cancle_run():
                global response
                response = 0
                messagebox_remove_many_root.destroy()
        
            #Remove many records
            def remove_many():
                global messagebox_remove_many_root
                messagebox_remove_many_root = customtkinter.CTk()
                messagebox_remove_many_root.geometry("450x150")

                messagebox_remove_many_text = customtkinter.CTkLabel(messagebox_remove_many_root, text = "Ovo će izbrisati označena polja iz baze podataka", font=('Arial', 23, 'bold'), text_color='#1F538D')
                messagebox_remove_many_text.place(x = 8, y = 15)

                messagebox_remove_many_button_ok = customtkinter.CTkButton(messagebox_remove_many_root, text = "Ok", command = messagebox_remove_many_ok_run)
                messagebox_remove_many_button_ok.place(x = 50, y = 80)

                messagebox_remove_many_button_cancle = customtkinter.CTkButton(messagebox_remove_many_root, text = "Odustani", command = messagebox_remove_many_cancle_run)
                messagebox_remove_many_button_cancle.place(x = 250, y = 80)

                messagebox_remove_many_root.mainloop()

            def messagebox_remove_all_ok_run():
                from connector import remove_all_data
                remove_all_data()

                for record in my_tree.get_children():
                    my_tree.delete(record)
                
                Id_Entry.delete(0, END)
                Ime_Entry.delete(0, END)
                Vrijeme_Entry.delete(0, END)
            
            def messagebox_remove_all_cancle_run():
                messagebox_remove_all_root.destroy()

            def remove_all():
                global messagebox_remove_all_root
                messagebox_remove_all_root = customtkinter.CTk()
                messagebox_remove_all_root.geometry("450x150")

                messagebox_remove_all_text = customtkinter.CTkLabel(messagebox_remove_all_root, text = "Izbrisat će se svi podaci u bazi podataka", font=('Arial', 23, 'bold'), text_color='#1F538D')
                messagebox_remove_all_text.place(x = 8, y = 15)

                messagebox_remove_all_button_ok = customtkinter.CTkButton(messagebox_remove_all_root, text = "Ok", command = messagebox_remove_all_ok_run)
                messagebox_remove_all_button_ok.place(x = 50, y = 80)

                messagebox_remove_all_button_cancle = customtkinter.CTkButton(messagebox_remove_all_root, text = "Odustani", command = messagebox_remove_all_cancle_run)
                messagebox_remove_all_button_cancle.place(x = 250, y = 80)

                messagebox_remove_all_root.mainloop()

            def update_records():
                selected = my_tree.focus()
                my_tree.item(selected, text = "", values = (Id_Entry.get(), Ime_Entry.get(), Vrijeme_Entry.get(),))
                
                Id_Entry.delete(0, END)
                Ime_Entry.delete(0, END)
                Vrijeme_Entry.delete(0, END) 

            def select_record(e):
                Id_Entry.delete(0, END)
                Ime_Entry.delete(0, END)
                Vrijeme_Entry.delete(0, END)

                selected = my_tree.focus()
                values = my_tree.item(selected, 'values')

                Id_Entry.insert(0, values[0])
                Ime_Entry.insert(0, values[1])
                Vrijeme_Entry.insert(0, values[2])

            def lookup_records():
                 global search_entry, search
                 search = Toplevel(root_Table)
                 search.config(background = '#282B34')
                 search.title("Tražilica")
                 search.geometry("400x200")

                 search.geometry("400x200")

                 text_datum_search_frame = customtkinter.CTkLabel(search, text = "Datum: ", font=('Arial', 23, 'bold'), text_color='#1F538D')
                 text_datum_search_frame.pack(padx = 10, pady = 10)

                 search_entry = customtkinter.CTkEntry(search, font = ("Helvetica", 18))
                 search_entry.pack(pady = 20, padx = 20)

                 search_button = customtkinter.CTkButton(search, text = "Traži", command = search_records)
                 search_button.pack(padx = 20, pady = 20)

            def search_records():
                lookup_record = search_entry.get()
                search.destroy()

                for record in my_tree.get_children():
                    my_tree.delete(record)

                from connector import search_records_data
                search_records_data(my_tree, root_Table, lookup_record)
                      
            
            Button_frame = customtkinter.CTkFrame(root_Table)
            Button_frame.pack(fill = "x", expand = "yes", padx = 20)

            text_commands_button_frame = customtkinter.CTkLabel(Button_frame, text = "Opcije", font=('Arial', 23, 'bold'), text_color='#1F538D')
            text_commands_button_frame.grid(row = 0, column = 0, padx = 10, pady = 10)

            Update_button = customtkinter.CTkButton(Button_frame, text = "Ažuriraj tablicu", command = update_records)
            Update_button.grid(row = 1, column = 0, padx = 10, pady = 10)

            Remove_all_button = customtkinter.CTkButton(Button_frame, text = "Izbriši sve podatke iz baze podataka", command = remove_all)
            Remove_all_button.grid(row = 1, column = 1, padx = 10, pady = 10)

            Remove_one_button = customtkinter.CTkButton(Button_frame, text = "Izbrši jedno označeno", command = remove_one)
            Remove_one_button.grid(row = 1, column = 2, padx = 10, pady = 10)

            Remove_many_button = customtkinter.CTkButton(Button_frame, text = "Izbriši označeno", command = remove_many)
            Remove_many_button.grid(row = 1, column = 3, padx = 10, pady = 10)

            Clear_button = customtkinter.CTkButton(Button_frame, text = "Očisti polja", command = clear_entries)
            Clear_button.grid(row = 1, column = 4, padx = 10, pady = 10)

            my_tree.bind("<ButtonRelease-1>", select_record)

            my_menu = Menu(root_Table)
            my_menu.config(background = '#c3c3c3')
            root_Table.config(menu=my_menu)

            search_menu = Menu(my_menu, tearoff=0)
            search_menu.config(background = '#c3c3c3')
            my_menu.add_cascade(label="Traži", menu=search_menu)

            search_menu.add_command(label="Traži", command=lookup_records)
            search_menu.add_separator()

            from connector import tree_pull_db
            tree_pull_db(my_tree, root_Table)

            root_Table.update()

def dolasci_table(one_frame, global_odabir_dvorana):
            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("dark-blue")

            dolasci_root_Table = customtkinter.CTk()
            dolasci_width_value=dolasci_root_Table.winfo_screenwidth()
            dolasci_height_value=dolasci_root_Table.winfo_screenheight()
            dolasci_root_Table.geometry("%dx%d-10+0" % (dolasci_width_value, dolasci_height_value-70))

            dolasci_style = ttk.Style()

            dolasci_style.theme_use('default')

            dolasci_style.configure('Threeview', background = '#D3D3D3', foreground = 'black', rowheight = 25, fieldbackground = '#D3D3D3')

            dolasci_style.map('Threeview', background = [('selected', '#3f7083')])

            dolasci_tree_frame = customtkinter.CTkFrame(dolasci_root_Table)
            dolasci_tree_frame.pack(pady = 20)

            dolasci_three_scroll = customtkinter.CTkScrollbar(dolasci_tree_frame, width = 20)
            dolasci_three_scroll.pack(side = RIGHT, fill = Y)

            global dolasci_my_tree
            dolasci_my_tree = ttk.Treeview(dolasci_tree_frame, yscrollcommand = dolasci_three_scroll.set, selectmode = 'extended', height = 25)
            dolasci_my_tree.pack()

            dolasci_three_scroll.configure(command = dolasci_my_tree.yview)

            dolasci_my_tree ['columns'] = ("Ime", "Dvorana", "Zapis", "Vrijeme")

            dolasci_my_tree.column("#0", width = 0, stretch = NO)
            dolasci_my_tree.column("Ime", anchor = W, width = 250)
            dolasci_my_tree.column("Dvorana", anchor = W, width = 250)
            dolasci_my_tree.column("Zapis", anchor = W, width = 250)
            dolasci_my_tree.column("Vrijeme", anchor = CENTER, width = 250)

            dolasci_my_tree.heading("#0", text = "", anchor = W)
            dolasci_my_tree.heading("Ime", text = "Ime", anchor = W)
            dolasci_my_tree.heading("Dvorana", text = "Dvorana", anchor = W)
            dolasci_my_tree.heading("Zapis", text = "Zapis", anchor = W)
            dolasci_my_tree.heading("Vrijeme", text = "Vrijeme", anchor = CENTER)

            dolasci_my_tree.tag_configure('oddrow', background = "white")
            dolasci_my_tree.tag_configure('evenrow', background = "lightblue")

            dolasci_data_frame = customtkinter.CTkFrame(dolasci_root_Table)
            dolasci_data_frame.pack(fill = 'x', expand = "yes", padx = 20)

            dolasci_textRecord_data_frame = customtkinter.CTkLabel (dolasci_data_frame, text = "Podaci", font=('Arial', 23, 'bold'), text_color='#1F538D')
            dolasci_textRecord_data_frame.grid(row = 0, column = 0, padx = 10, pady = 10)

            dolasci_Ime_Label = customtkinter.CTkLabel(dolasci_data_frame, text = "Ime: ")
            dolasci_Ime_Label.grid(row = 1, column = 0, padx = 10, pady = 10)
            dolasci_Ime_Entry = customtkinter.CTkEntry(dolasci_data_frame)
            dolasci_Ime_Entry.grid(row = 1, column = 1, padx = 10, pady = 10)

            dolasci_Dvorana_Label = customtkinter.CTkLabel(dolasci_data_frame, text = "Dvorana: ")
            dolasci_Dvorana_Label.grid(row = 1, column = 2, padx = 10, pady = 10)
            dolasci_Dvorana_Entry = customtkinter.CTkEntry(dolasci_data_frame)
            dolasci_Dvorana_Entry.grid(row = 1, column = 3, padx = 10, pady = 10)

            dolasci_Zapis_Label = customtkinter.CTkLabel(dolasci_data_frame, text = "Zapis: ")
            dolasci_Zapis_Label.grid(row = 1, column = 4, padx = 10, pady = 10)
            dolasci_Zapis_Entry = customtkinter.CTkEntry(dolasci_data_frame)
            dolasci_Zapis_Entry.grid(row = 1, column = 5, padx = 10, pady = 10)

            dolasci_Vrijeme_Label = customtkinter.CTkLabel(dolasci_data_frame, text = "Vrijeme: ")
            dolasci_Vrijeme_Label.grid(row = 1, column = 6, padx = 10, pady = 10)
            dolasci_Vrijeme_Entry = customtkinter.CTkEntry(dolasci_data_frame)
            dolasci_Vrijeme_Entry.grid(row = 1, column = 7, padx = 10, pady = 10)

            def select_record(e):
                dolasci_Ime_Entry.delete(0, END)
                dolasci_Dvorana_Entry.delete(0, END)
                dolasci_Zapis_Entry.delete(0, END)
                dolasci_Vrijeme_Entry.delete(0, END)

                selected = dolasci_my_tree.focus()
                values = dolasci_my_tree.item(selected, 'values')

                dolasci_Ime_Entry.insert(0, values[0])
                dolasci_Dvorana_Entry.insert(0, values[1])
                dolasci_Zapis_Entry.insert(0, values[2])
                dolasci_Vrijeme_Entry.insert(0, values[3])

            def lookup_records():
                 global ime_dolasci_search_entry, dvorana_dolasci_search_entry, date_dolasci_search_entry, dolasci_search
                 ime_dolasci_search_entry = " "
                 dvorana_dolasci_search_entry = " "
                 date_dolasci_search_entry = " "
                 dolasci_search = Toplevel(dolasci_root_Table)
                 dolasci_search.config(background = '#282B34')
                 dolasci_search.title("Tražilica")
                 dolasci_search.geometry("600x300")

                 ime_search_label = customtkinter.CTkLabel(dolasci_search, text = "Ime: ", font=('Arial', 23, 'bold'), text_color='#1F538D')
                 ime_search_label.place(x = 100, y = 50)

                 ime_dolasci_search_entry = customtkinter.CTkEntry(dolasci_search, font = ("Helvetica", 18))
                 ime_dolasci_search_entry.place(x = 300, y = 50)

                 dvorana_search_label = customtkinter.CTkLabel(dolasci_search, text = "Dvorana: ", font=('Arial', 23, 'bold'), text_color='#1F538D')
                 dvorana_search_label.place(x = 100, y = 100)

                 dvorana_dolasci_search_entry = customtkinter.CTkEntry(dolasci_search, font = ("Helvetica", 18))
                 dvorana_dolasci_search_entry.place(x = 300, y = 100)

                 date_search_label = customtkinter.CTkLabel(dolasci_search, text = "Datum: ", font=('Arial', 23, 'bold'), text_color='#1F538D')
                 date_search_label.place(x = 100, y = 150)

                 date_dolasci_search_entry = customtkinter.CTkEntry(dolasci_search, font = ("Helvetica", 18))
                 date_dolasci_search_entry.place(x = 300, y = 150)

                 search_button = customtkinter.CTkButton(dolasci_search, text = "Pretraži", command = search_records)
                 search_button.place(x = 230, y = 230)

            def search_records():
                lookup_record_ime = ime_dolasci_search_entry.get()
                lookup_record_dvorana = dvorana_dolasci_search_entry.get()
                lookup_record_date = date_dolasci_search_entry.get()
                dolasci_search.destroy()

                for record in dolasci_my_tree.get_children():
                    dolasci_my_tree.delete(record)

                from connector import dolasci_search_records_data
                dolasci_search_records_data(dolasci_my_tree, dolasci_root_Table, lookup_record_ime, lookup_record_dvorana, lookup_record_date, global_odabir_dvorana)
                      
            
            def izbisi_iz_tablice():
                 for record in dolasci_my_tree.get_children():
                    dolasci_my_tree.delete(record)

                 from connector import dolasci_tree_pull_db
                 dolasci_tree_pull_db(dolasci_my_tree, dolasci_root_Table, global_odabir_dvorana)


            dolasci_Button_frame = customtkinter.CTkFrame(dolasci_root_Table, width=300, height=600)
            dolasci_Button_frame.place(x=20, y=20)

            dolasci_trazi_button = customtkinter.CTkButton(dolasci_Button_frame, text = "Pretraži", width=150, height=50, command = lookup_records)
            dolasci_trazi_button.place(x=75, y=30)

            from connector import dolasci_tree_pull_db

            azuriraj_button = customtkinter.CTkButton(dolasci_Button_frame, text = "Ažuriraj tablicu", width=150, height=50, command = izbisi_iz_tablice)
            azuriraj_button.place(x=75, y=100)

            dolasci_my_tree.bind("<ButtonRelease-1>", select_record)

            my_menu = Menu(dolasci_root_Table)
            my_menu.config(background = '#c3c3c3')
            dolasci_root_Table.config(menu=my_menu)

            search_menu = Menu(my_menu, tearoff=0)
            search_menu.config(background = '#c3c3c3')
            my_menu.add_cascade(label="Traži", menu=search_menu)

            search_menu.add_command(label="Traži", command=lookup_records)
            search_menu.add_separator()

            from connector import dolasci_tree_pull_db
            dolasci_tree_pull_db(dolasci_my_tree, dolasci_root_Table, global_odabir_dvorana)

            dolasci_root_Table.update()

def odlasci_table(one_frame, global_odabir_dvorana):
            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("dark-blue")

            odlasci_root_Table = customtkinter.CTk()
            odlasci_width_value=odlasci_root_Table.winfo_screenwidth()
            odlasci_height_value=odlasci_root_Table.winfo_screenheight()
            odlasci_root_Table.geometry("%dx%d-10+0" % (odlasci_width_value, odlasci_height_value-70))

            odlasci_style = ttk.Style()

            odlasci_style.theme_use('default')

            odlasci_style.configure('Threeview', background = '#D3D3D3', foreground = 'black', rowheight = 25, fieldbackground = '#D3D3D3')

            odlasci_style.map('Threeview', background = [('selected', '#3f7083')])

            dolasci_tree_frame = customtkinter.CTkFrame(odlasci_root_Table)
            dolasci_tree_frame.pack(pady = 20)

            dolasci_three_scroll = customtkinter.CTkScrollbar(dolasci_tree_frame, width = 20)
            dolasci_three_scroll.pack(side = RIGHT, fill = Y)

            global odlasci_my_tree
            odlasci_my_tree = ttk.Treeview(dolasci_tree_frame, yscrollcommand = dolasci_three_scroll.set, selectmode = 'extended', height = 25)
            odlasci_my_tree.pack()

            dolasci_three_scroll.configure(command = odlasci_my_tree.yview)

            odlasci_my_tree ['columns'] = ("Ime", "Dvorana", "Zapis", "Vrijeme")

            odlasci_my_tree.column("#0", width = 0, stretch = NO)
            odlasci_my_tree.column("Ime", anchor = W, width = 250)
            odlasci_my_tree.column("Dvorana", anchor = W, width = 250)
            odlasci_my_tree.column("Zapis", anchor = W, width = 250)
            odlasci_my_tree.column("Vrijeme", anchor = CENTER, width = 250)

            odlasci_my_tree.heading("#0", text = "", anchor = W)
            odlasci_my_tree.heading("Ime", text = "Ime", anchor = W)
            odlasci_my_tree.heading("Dvorana", text = "Dvorana", anchor = W)
            odlasci_my_tree.heading("Zapis", text = "Zapis", anchor = W)
            odlasci_my_tree.heading("Vrijeme", text = "Vrijeme", anchor = CENTER)

            odlasci_my_tree.tag_configure('oddrow', background = "white")
            odlasci_my_tree.tag_configure('evenrow', background = "lightblue")

            dolasci_data_frame = customtkinter.CTkFrame(odlasci_root_Table)
            dolasci_data_frame.pack(fill = 'x', expand = "yes", padx = 20)

            dolasci_textRecord_data_frame = customtkinter.CTkLabel (dolasci_data_frame, text = "Podaci", font=('Arial', 23, 'bold'), text_color='#1F538D')
            dolasci_textRecord_data_frame.grid(row = 0, column = 0, padx = 10, pady = 10)

            dolasci_Ime_Label = customtkinter.CTkLabel(dolasci_data_frame, text = "Ime: ")
            dolasci_Ime_Label.grid(row = 1, column = 0, padx = 10, pady = 10)
            dolasci_Ime_Entry = customtkinter.CTkEntry(dolasci_data_frame)
            dolasci_Ime_Entry.grid(row = 1, column = 1, padx = 10, pady = 10)

            dolasci_Dvorana_Label = customtkinter.CTkLabel(dolasci_data_frame, text = "Dvorana: ")
            dolasci_Dvorana_Label.grid(row = 1, column = 2, padx = 10, pady = 10)
            dolasci_Dvorana_Entry = customtkinter.CTkEntry(dolasci_data_frame)
            dolasci_Dvorana_Entry.grid(row = 1, column = 3, padx = 10, pady = 10)

            dolasci_Zapis_Label = customtkinter.CTkLabel(dolasci_data_frame, text = "Zapis: ")
            dolasci_Zapis_Label.grid(row = 1, column = 4, padx = 10, pady = 10)
            dolasci_Zapis_Entry = customtkinter.CTkEntry(dolasci_data_frame)
            dolasci_Zapis_Entry.grid(row = 1, column = 5, padx = 10, pady = 10)

            dolasci_Vrijeme_Label = customtkinter.CTkLabel(dolasci_data_frame, text = "Vrijeme: ")
            dolasci_Vrijeme_Label.grid(row = 1, column = 6, padx = 10, pady = 10)
            dolasci_Vrijeme_Entry = customtkinter.CTkEntry(dolasci_data_frame)
            dolasci_Vrijeme_Entry.grid(row = 1, column = 7, padx = 10, pady = 10)

            def select_record(e):
                dolasci_Ime_Entry.delete(0, END)
                dolasci_Dvorana_Entry.delete(0, END)
                dolasci_Zapis_Entry.delete(0, END)
                dolasci_Vrijeme_Entry.delete(0, END)

                selected = odlasci_my_tree.focus()
                values = odlasci_my_tree.item(selected, 'values')

                dolasci_Ime_Entry.insert(0, values[0])
                dolasci_Dvorana_Entry.insert(0, values[1])
                dolasci_Zapis_Entry.insert(0, values[2])
                dolasci_Vrijeme_Entry.insert(0, values[3])

            def lookup_records():
                 global ime_odlasci_search_entry, dvorana_odlasci_search_entry, date_odlasci_search_entry, dolasci_search
                 ime_odlasci_search_entry = " "
                 dvorana_odlasci_search_entry = " "
                 date_odlasci_search_entry = " "
                 dolasci_search = Toplevel(odlasci_root_Table)
                 dolasci_search.config(background = '#282B34')
                 dolasci_search.title("Tražilica")
                 dolasci_search.geometry("600x300")

                 ime_search_label = customtkinter.CTkLabel(dolasci_search, text = "Ime: ", font=('Arial', 23, 'bold'), text_color='#1F538D')
                 ime_search_label.place(x = 100, y = 50)

                 ime_odlasci_search_entry = customtkinter.CTkEntry(dolasci_search, font = ("Helvetica", 18))
                 ime_odlasci_search_entry.place(x = 300, y = 50)

                 dvorana_search_label = customtkinter.CTkLabel(dolasci_search, text = "Dvorana: ", font=('Arial', 23, 'bold'), text_color='#1F538D')
                 dvorana_search_label.place(x = 100, y = 100)

                 dvorana_odlasci_search_entry = customtkinter.CTkEntry(dolasci_search, font = ("Helvetica", 18))
                 dvorana_odlasci_search_entry.place(x = 300, y = 100)

                 date_search_label = customtkinter.CTkLabel(dolasci_search, text = "Datum: ", font=('Arial', 23, 'bold'), text_color='#1F538D')
                 date_search_label.place(x = 100, y = 150)

                 date_odlasci_search_entry = customtkinter.CTkEntry(dolasci_search, font = ("Helvetica", 18))
                 date_odlasci_search_entry.place(x = 300, y = 150)

                 search_button = customtkinter.CTkButton(dolasci_search, text = "Pretraži", command = search_records)
                 search_button.place(x = 230, y = 230)

            def search_records():
                lookup_record_ime = ime_odlasci_search_entry.get()
                lookup_record_dvorana = dvorana_odlasci_search_entry.get()
                lookup_record_date = date_odlasci_search_entry.get()
                dolasci_search.destroy()

                for record in odlasci_my_tree.get_children():
                    odlasci_my_tree.delete(record)

                from connector import odlasci_search_records_data
                odlasci_search_records_data(odlasci_my_tree, odlasci_root_Table, lookup_record_ime, lookup_record_dvorana, lookup_record_date, global_odabir_dvorana)
                      
            
            def izbisi_iz_tablice():
                 for record in odlasci_my_tree.get_children():
                    odlasci_my_tree.delete(record)

                 from connector import odlasci_tree_pull_db
                 odlasci_tree_pull_db(odlasci_my_tree, odlasci_root_Table, global_odabir_dvorana)


            dolasci_Button_frame = customtkinter.CTkFrame(odlasci_root_Table, width=300, height=600)
            dolasci_Button_frame.place(x=20, y=20)

            dolasci_trazi_button = customtkinter.CTkButton(dolasci_Button_frame, text = "Pretraži", width=150, height=50, command = lookup_records)
            dolasci_trazi_button.place(x=75, y=30)

            azuriraj_button = customtkinter.CTkButton(dolasci_Button_frame, text = "Ažuriraj tablicu", width=150, height=50, command = izbisi_iz_tablice)
            azuriraj_button.place(x=75, y=100)

            odlasci_my_tree.bind("<ButtonRelease-1>", select_record)

            my_menu = Menu(odlasci_root_Table)
            my_menu.config(background = '#c3c3c3')
            odlasci_root_Table.config(menu=my_menu)

            search_menu = Menu(my_menu, tearoff=0)
            search_menu.config(background = '#c3c3c3')
            my_menu.add_cascade(label="Traži", menu=search_menu)

            search_menu.add_command(label="Traži", command=lookup_records)
            search_menu.add_separator()

            from connector import odlasci_tree_pull_db
            odlasci_tree_pull_db(odlasci_my_tree, odlasci_root_Table, global_odabir_dvorana)

            odlasci_root_Table.update()

def svi_zapisi_table(one_frame):
            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("dark-blue")

            odlasci_root_Table = customtkinter.CTk()
            odlasci_width_value=odlasci_root_Table.winfo_screenwidth()
            odlasci_height_value=odlasci_root_Table.winfo_screenheight()
            odlasci_root_Table.geometry("%dx%d-10+0" % (odlasci_width_value, odlasci_height_value-70))

            odlasci_style = ttk.Style()

            odlasci_style.theme_use('default')

            odlasci_style.configure('Threeview', background = '#D3D3D3', foreground = 'black', rowheight = 25, fieldbackground = '#D3D3D3')

            odlasci_style.map('Threeview', background = [('selected', '#3f7083')])

            dolasci_tree_frame = customtkinter.CTkFrame(odlasci_root_Table)
            dolasci_tree_frame.pack(pady = 20)

            dolasci_three_scroll = customtkinter.CTkScrollbar(dolasci_tree_frame, width = 20)
            dolasci_three_scroll.pack(side = RIGHT, fill = Y)

            global svi_zapisi_my_tree
            svi_zapisi_my_tree = ttk.Treeview(dolasci_tree_frame, yscrollcommand = dolasci_three_scroll.set, selectmode = 'extended', height = 25)
            svi_zapisi_my_tree.pack()

            dolasci_three_scroll.configure(command = svi_zapisi_my_tree.yview)

            svi_zapisi_my_tree ['columns'] = ("Ime", "Dvorana", "Zapis", "Vrijeme")

            svi_zapisi_my_tree.column("#0", width = 0, stretch = NO)
            svi_zapisi_my_tree.column("Ime", anchor = W, width = 250)
            svi_zapisi_my_tree.column("Dvorana", anchor = W, width = 250)
            svi_zapisi_my_tree.column("Zapis", anchor = W, width = 250)
            svi_zapisi_my_tree.column("Vrijeme", anchor = CENTER, width = 250)

            svi_zapisi_my_tree.heading("#0", text = "", anchor = W)
            svi_zapisi_my_tree.heading("Ime", text = "Ime", anchor = W)
            svi_zapisi_my_tree.heading("Dvorana", text = "Dvorana", anchor = W)
            svi_zapisi_my_tree.heading("Zapis", text = "Zapis", anchor = W)
            svi_zapisi_my_tree.heading("Vrijeme", text = "Vrijeme", anchor = CENTER)

            svi_zapisi_my_tree.tag_configure('oddrow', background = "white")
            svi_zapisi_my_tree.tag_configure('evenrow', background = "lightblue")

            dolasci_data_frame = customtkinter.CTkFrame(odlasci_root_Table)
            dolasci_data_frame.pack(fill = 'x', expand = "yes", padx = 20)

            dolasci_textRecord_data_frame = customtkinter.CTkLabel (dolasci_data_frame, text = "Podaci", font=('Arial', 23, 'bold'), text_color='#1F538D')
            dolasci_textRecord_data_frame.grid(row = 0, column = 0, padx = 10, pady = 10)

            dolasci_Ime_Label = customtkinter.CTkLabel(dolasci_data_frame, text = "Ime: ")
            dolasci_Ime_Label.grid(row = 1, column = 0, padx = 10, pady = 10)
            dolasci_Ime_Entry = customtkinter.CTkEntry(dolasci_data_frame)
            dolasci_Ime_Entry.grid(row = 1, column = 1, padx = 10, pady = 10)

            dolasci_Dvorana_Label = customtkinter.CTkLabel(dolasci_data_frame, text = "Dvorana: ")
            dolasci_Dvorana_Label.grid(row = 1, column = 2, padx = 10, pady = 10)
            dolasci_Dvorana_Entry = customtkinter.CTkEntry(dolasci_data_frame)
            dolasci_Dvorana_Entry.grid(row = 1, column = 3, padx = 10, pady = 10)

            dolasci_Zapis_Label = customtkinter.CTkLabel(dolasci_data_frame, text = "Zapis: ")
            dolasci_Zapis_Label.grid(row = 1, column = 4, padx = 10, pady = 10)
            dolasci_Zapis_Entry = customtkinter.CTkEntry(dolasci_data_frame)
            dolasci_Zapis_Entry.grid(row = 1, column = 5, padx = 10, pady = 10)

            dolasci_Vrijeme_Label = customtkinter.CTkLabel(dolasci_data_frame, text = "Vrijeme: ")
            dolasci_Vrijeme_Label.grid(row = 1, column = 6, padx = 10, pady = 10)
            dolasci_Vrijeme_Entry = customtkinter.CTkEntry(dolasci_data_frame)
            dolasci_Vrijeme_Entry.grid(row = 1, column = 7, padx = 10, pady = 10)

            def select_record(e):
                dolasci_Ime_Entry.delete(0, END)
                dolasci_Dvorana_Entry.delete(0, END)
                dolasci_Zapis_Entry.delete(0, END)
                dolasci_Vrijeme_Entry.delete(0, END)

                selected = svi_zapisi_my_tree.focus()
                values = svi_zapisi_my_tree.item(selected, 'values')

                dolasci_Ime_Entry.insert(0, values[0])
                dolasci_Dvorana_Entry.insert(0, values[1])
                dolasci_Zapis_Entry.insert(0, values[2])
                dolasci_Vrijeme_Entry.insert(0, values[3])

            def lookup_records():
                 global ime_svi_zapisi_search_entry, dvorana_svi_zapisi_search_entry, date_svi_zapisi_search_entry, zapis_svi_zapisi_search_entry, svi_zapisi_search
                 ime_svi_zapisi_search_entry = " "
                 dvorana_svi_zapisi_search_entry = " "
                 zapis_svi_zapisi_search_entry = " "
                 date_svi_zapisi_search_entry = " "
                 svi_zapisi_search = Toplevel(odlasci_root_Table)
                 svi_zapisi_search.config(background = '#282B34')
                 svi_zapisi_search.title("Tražilica")
                 svi_zapisi_search.geometry("600x350")

                 ime_search_label = customtkinter.CTkLabel(svi_zapisi_search, text = "Ime: ", font=('Arial', 23, 'bold'), text_color='#1F538D')
                 ime_search_label.place(x = 100, y = 50)

                 ime_svi_zapisi_search_entry = customtkinter.CTkEntry(svi_zapisi_search, font = ("Helvetica", 18))
                 ime_svi_zapisi_search_entry.place(x = 300, y = 50)

                 dvorana_search_label = customtkinter.CTkLabel(svi_zapisi_search, text = "Dvorana: ", font=('Arial', 23, 'bold'), text_color='#1F538D')
                 dvorana_search_label.place(x = 100, y = 100)

                 dvorana_svi_zapisi_search_entry = customtkinter.CTkEntry(svi_zapisi_search, font = ("Helvetica", 18))
                 dvorana_svi_zapisi_search_entry.place(x = 300, y = 100)

                 zapis_svi_zapisi_search_label = customtkinter.CTkLabel(svi_zapisi_search, text = "Zapis: ", font=('Arial', 23, 'bold'), text_color='#1F538D')
                 zapis_svi_zapisi_search_label.place(x = 100, y = 150)

                 zapis_svi_zapisi_search_entry = customtkinter.CTkEntry(svi_zapisi_search, font = ("Helvetica", 18))
                 zapis_svi_zapisi_search_entry.place(x = 300, y = 150)

                 date_search_label = customtkinter.CTkLabel(svi_zapisi_search, text = "Datum: ", font=('Arial', 23, 'bold'), text_color='#1F538D')
                 date_search_label.place(x = 100, y = 200)

                 date_svi_zapisi_search_entry = customtkinter.CTkEntry(svi_zapisi_search, font = ("Helvetica", 18))
                 date_svi_zapisi_search_entry.place(x = 300, y = 200)

                 search_button = customtkinter.CTkButton(svi_zapisi_search, text = "Pretraži", command = search_records)
                 search_button.place(x = 230, y = 280)

            def search_records():
                lookup_record_ime = ime_svi_zapisi_search_entry.get()
                lookup_record_dvorana = dvorana_svi_zapisi_search_entry.get()
                lookup_record_zapis = zapis_svi_zapisi_search_entry.get()
                lookup_record_date = date_svi_zapisi_search_entry.get()
                svi_zapisi_search.destroy()

                for record in svi_zapisi_my_tree.get_children():
                    svi_zapisi_my_tree.delete(record)

                from connector import svi_zapisi_search_records_data
                svi_zapisi_search_records_data(svi_zapisi_my_tree, odlasci_root_Table, lookup_record_ime, lookup_record_dvorana, lookup_record_date, lookup_record_zapis)
                      
            
            def izbisi_iz_tablice():
                 for record in svi_zapisi_my_tree.get_children():
                    svi_zapisi_my_tree.delete(record)

                 from connector import svi_zapisi_tree_pull_db
                 svi_zapisi_tree_pull_db(svi_zapisi_my_tree, odlasci_root_Table)


            dolasci_Button_frame = customtkinter.CTkFrame(odlasci_root_Table, width=300, height=600)
            dolasci_Button_frame.place(x=20, y=20)

            dolasci_trazi_button = customtkinter.CTkButton(dolasci_Button_frame, text = "Pretraži", width=150, height=50, command = lookup_records)
            dolasci_trazi_button.place(x=75, y=30)

            azuriraj_button = customtkinter.CTkButton(dolasci_Button_frame, text = "Ažuriraj tablicu", width=150, height=50, command = izbisi_iz_tablice)
            azuriraj_button.place(x=75, y=100)

            svi_zapisi_my_tree.bind("<ButtonRelease-1>", select_record)

            my_menu = Menu(odlasci_root_Table)
            my_menu.config(background = '#c3c3c3')
            odlasci_root_Table.config(menu=my_menu)

            search_menu = Menu(my_menu, tearoff=0)
            search_menu.config(background = '#c3c3c3')
            my_menu.add_cascade(label="Traži", menu=search_menu)

            search_menu.add_command(label="Traži", command=lookup_records)
            search_menu.add_separator()

            from connector import svi_zapisi_tree_pull_db
            svi_zapisi_tree_pull_db(svi_zapisi_my_tree, odlasci_root_Table)

            odlasci_root_Table.update()

def Data_Page(Right_frame, MainWindow_btn, Data_btn, Settings_btn, stop_thread):
    MainWindow_btn.configure(state='normal')
    Data_btn.configure(state='disabled')
    Settings_btn.configure(state='normal')

    global is_on
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "files", "config.ini"))
    parser = ConfigParser()
    parser.read(filepath)
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

    current_dir = os.getcwd()
    UknowFaces_dir = "files/UknowFaces/"
    UknowFaces_fin_dir = os.path.join(current_dir, UknowFaces_dir)
    Faces_dir = "files/faces/"
    Faces_fin_dir = os.path.join(current_dir, Faces_dir)

    Path_connectors = os.path.abspath("connectors")
    sys.path.append(Path_connectors)

    def nepoznata_licabrowseFiles():
                filename = filedialog.askopenfilename(initialdir = UknowFaces_fin_dir,
                                                            title = "Select a File",
                                                            filetypes = [("All files", "*.*")])

    def poznata_licabrowseFiles():
                filename = filedialog.askopenfilename(initialdir = Faces_fin_dir,
                                                            title = "Select a File",
                                                            filetypes = [("All files", "*.*")])
                
    def trainer():
        from trainner import trainner_start
        trainner_start()

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

    one_frame = customtkinter.CTkFrame(Right_frame, width=679, height=389)
    one_frame.place(x=10, y=0)

    title_one_frame = customtkinter.CTkLabel(one_frame, text='Vrijeme zabilježenja lica', fg_color="gray30", font=('Bold', 30), corner_radius=6)
    title_one_frame.place(x=200, y=0)

    one_label_text = customtkinter.CTkLabel(one_frame, text='Lista tablice iz baze podataka', font=('normal', 14))
    one_label_text.place(x=15, y=80)

    one_frame_btn = customtkinter.CTkButton(one_frame, text='Pokaži', font=('Bold', 17), width=150, height=40,  fg_color='#2B719E', command=lambda: Test(one_frame)) # command=lambda: indicate(MainWindow_btn_page)
    one_frame_btn.place(x=300, y=75)

    two_frame = customtkinter.CTkFrame(Right_frame, width=679, height=389)
    two_frame.place(x=699, y=0)

    title_two_frame = customtkinter.CTkLabel(two_frame, text='Slike lica', fg_color="gray30", font=('Bold', 30), corner_radius=6)
    title_two_frame.place(x=320, y=0)

    nepoznata_lica_btn = customtkinter.CTkButton(two_frame, text = "Nepoznata lica", font=('Bold', 17), width=150, height=40,  fg_color='#2B719E', command = nepoznata_licabrowseFiles)
    nepoznata_lica_btn.place(x=300, y=75)

    poznata_lica_btn = customtkinter.CTkButton(two_frame, text = "Poznata lica", font=('Bold', 17), width=150, height=40,  fg_color='#2B719E', command = poznata_licabrowseFiles)
    poznata_lica_btn.place(x=300, y=175)

    three_frame = customtkinter.CTkFrame(Right_frame, width=679, height=389)
    three_frame.place(x=10, y=399)

    title_three_frame = customtkinter.CTkLabel(three_frame, text='Zapis ljudi', fg_color="gray30", font=('Bold', 30), corner_radius=6)
    title_three_frame.place(x=320, y=0)

    combobox_var = "Dvorana 309"
    combobox = customtkinter.CTkComboBox(three_frame, values=["Dvorana 2", "Dvorana 303", "Dvorana 309", "Dvorana 311", "Dvorana 312"],
                                        state = "readonly", command=combobox_callback)
    combobox.set("Dvorana 309")
    combobox.place(x=320, y=75)
    combobox_callback(combobox_var)

    dolazak_btn = customtkinter.CTkButton(three_frame, text='Dolasci', font=('Bold', 17), width=150, height=40,  fg_color='#2B719E', command=lambda: dolasci_table(one_frame, global_odabir_dvorana)) # command=lambda: indicate(MainWindow_btn_page)
    dolazak_btn.place(x=320, y=130)

    odlazak_btn = customtkinter.CTkButton(three_frame, text='Odlasci', font=('Bold', 17), width=150, height=40,  fg_color='#2B719E', command=lambda: odlasci_table(one_frame, global_odabir_dvorana)) # command=lambda: indicate(MainWindow_btn_page)
    odlazak_btn.place(x=320, y=200)

    zajednicko_btn = customtkinter.CTkButton(three_frame, text='Svi zapisi', font=('Bold', 17), width=150, height=40,  fg_color='#2B719E', command=lambda: svi_zapisi_table(one_frame)) # command=lambda: indicate(MainWindow_btn_page)
    zajednicko_btn.place(x=320, y=270)

    four_frame = customtkinter.CTkFrame(Right_frame, width=679, height=389)
    four_frame.place(x=699, y=399)

    title_four_frame = customtkinter.CTkLabel(four_frame, text='Učenje lica', fg_color="gray30", font=('Bold', 30), corner_radius=6)
    title_four_frame.place(x=320, y=0)

    four_frame_btn = customtkinter.CTkButton(four_frame, text='Pokreni', font=('Bold', 17), width=150, height=40,  fg_color='#2B719E', command = trainer) # command=lambda: indicate(MainWindow_btn_page)
    four_frame_btn.place(x=320, y=339)