import mysql.connector
import customtkinter
from configparser import ConfigParser
from os import path
import sys
import os

Path_Windows = os.path.abspath("windows")
sys.path.append(Path_Windows)

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, ".." ,"files", "config.ini"))

parser = ConfigParser()
parser.read(filepath)

host_load_config=parser.get('database', 'host_set')
database_load_config=parser.get('database', 'database_set')
user_load_config=parser.get('database', 'user_set')
password_load_config=parser.get('database', 'password_set')

my_conn = mysql.connector.connect(
            host=host_load_config,
            database=database_load_config,
            user=user_load_config,
            password=password_load_config
            )

my_cursor = my_conn.cursor()

def open_conn():
    global my_cursor, my_conn

    try:
        from login import start_login
        start_login()

    except mysql.connector.Error as e:
        print("Error", e)

        global Invlogin_database
        Invlogin_database = customtkinter.CTk()

        frameInvlogin_database = customtkinter.CTkFrame(master=Invlogin_database)
        frameInvlogin_database.pack(pady=20, padx=60, fill="both", expand=True)

        label_login_database = customtkinter.CTkLabel(master=frameInvlogin_database, text="Netočno korisničko ime ili lozinka")
        label_login_database.pack(pady=12, padx=10)

        buttonInvlogin_database = customtkinter.CTkButton(master=frameInvlogin_database, text="OK", command=Inv_database)
        buttonInvlogin_database.pack(pady=12, padx=10)

        Invlogin_database.mainloop()

def close_conn():
    my_conn.close()
    print("MySQL connection is closed")

def Inv_database():
        Invlogin_database.destroy()
        from login import database_window_login
        database_window_login()

def login_connector(root, Username, Password):
    def Inv():
        InvCred.destroy()

    try:
        my_cursor = my_conn.cursor()
        sql = "SELECT * FROM login WHERE Username = '%s' AND Password = '%s'" % (Username.get(), Password.get())
        my_cursor.execute(sql)

        if my_cursor.fetchone():
            print("Prijava uspješna")
            root.destroy()
            from windows import MainWindow

        else:
            print("Netočno korisničko ime ili lozinka")
            global InvCred
            InvCred = customtkinter.CTk()

            frameInvCred = customtkinter.CTkFrame(master=InvCred)
            frameInvCred.pack(pady=20, padx=60, fill="both", expand=True)

            label = customtkinter.CTkLabel(master=frameInvCred, text="Netočno korisničko ime ili lozinka")
            label.pack(pady=12, padx=10)

            buttonInvCred = customtkinter.CTkButton(master=frameInvCred, text="OK", command=Inv)
            buttonInvCred.pack(pady=12, padx=10)

            InvCred.mainloop()

    except mysql.connector.Error as e:
        print("Error", e)


def insert_osobe_to_db():
    basepath = path.dirname(__file__)
    path_osobe = path.abspath(path.join(basepath, "..", "files", "faces"))
    dir_list = os.listdir(path_osobe)

    for i, element in enumerate(dir_list):
        globals()['variable{}'.format(i+1)] = element
    
    for i in range(1, len(dir_list)+1):
        print(globals()['variable{}'.format(i)])
        mor = globals()['variable{}'.format(i)]

        try:
            sql = "INSERT INTO osobe (Ime) SELECT ('%s') FROM dual WHERE NOT EXISTS (SELECT * FROM osobe WHERE ime =('%s') LIMIT 1)" % (mor, mor)
            my_cursor.execute(sql)
            my_conn.commit()

        except mysql.connector.Error as error:
            print("Failed to insert record into lica table {}".format(error))

def Insert_to_db(predict_name):  
    parser = ConfigParser()
    parser.read(filepath)
    dvorane_load_config=parser.get('dvorane', 'dvorana')
    try:    
        mySql_insert_query = "INSERT INTO dolazak (ID_osobe, Dvorana, Zapis) SELECT ID_osobe, ('%s'), 'Dolazak' FROM osobe WHERE Ime=('%s')" % (dvorane_load_config, predict_name)
        insert_lica = "INSERT INTO lica (username) VALUES ('%s')" % (predict_name)

        my_cursor.execute(mySql_insert_query)
        my_conn.commit()

        my_cursor.execute(insert_lica)
        my_conn.commit()
        print(my_cursor.rowcount, "Record inserted successfully into lica table")

    except mysql.connector.Error as error:
        print("Failed to insert record into lica table {}".format(error))

    finally:
        if (my_conn.is_connected()):
            print(predict_name)

def Insert_to_db2(predict_name2):  
    parser = ConfigParser()
    parser.read(filepath)
    dvorane_load_config=parser.get('dvorane', 'dvorana')
    try:    
        mySql_insert_query = "INSERT INTO Odlazak (ID_osobe, Dvorana, Zapis) SELECT ID_osobe, ('%s'), 'Odlazak' FROM osobe WHERE Ime=('%s')" % (dvorane_load_config, predict_name2)
        insert_lica = "INSERT INTO lica (username) VALUES ('%s')" % (predict_name2)

        my_cursor.execute(mySql_insert_query)
        my_conn.commit()

        my_cursor.execute(insert_lica)
        my_conn.commit()
        print(my_cursor.rowcount, "Record inserted successfully into lica table")

    except mysql.connector.Error as error:
        print("Failed to insert record into lica table {}".format(error))

    finally:
        if (my_conn.is_connected()):
            print(predict_name2)

def tree_pull_db(my_tree, root_Table):
    try:    
        my_cursor.execute("SELECT * FROM lica ORDER BY date DESC")
        records = my_cursor.fetchall()
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent = '', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2]), tags = ('evenrow',))
            else:
                my_tree.insert(parent = '', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2]), tags = ('oddrow',))

            count += 1

        root_Table.update()

    except Exception as e:
        print("Error", e)

def dolasci_tree_pull_db(my_tree, root_Table, odabir_dvorana):
    print(odabir_dvorana)
    try:    
        my_cursor.execute("SELECT osobe.Ime, dolazak.Dvorana, dolazak.Zapis, dolazak.Date FROM dolazak JOIN osobe ON dolazak.ID_osobe = osobe.ID_osobe WHERE Dvorana like '%" + odabir_dvorana + "%' ORDER BY Date DESC")
        records = my_cursor.fetchall()
        dolasci_count = 0

        for record in records:
            if dolasci_count % 2 == 0:
                my_tree.insert(parent = '', index = 'end', iid = dolasci_count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
            else:
                my_tree.insert(parent = '', index = 'end', iid = dolasci_count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

            dolasci_count += 1

        root_Table.update()

    except Exception as e:
        print("Error", e)

def odlasci_tree_pull_db(my_tree, root_Table, odabir_dvorana):
    print(odabir_dvorana)
    try:    
        my_cursor.execute("SELECT osobe.Ime, Odlazak.Dvorana, Odlazak.Zapis, Odlazak.Date FROM Odlazak JOIN osobe ON Odlazak.ID_osobe = osobe.ID_osobe WHERE Dvorana like '%" + odabir_dvorana + "%' ORDER BY Date DESC")
        records = my_cursor.fetchall()
        dolasci_count = 0

        for record in records:
            if dolasci_count % 2 == 0:
                my_tree.insert(parent = '', index = 'end', iid = dolasci_count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
            else:
                my_tree.insert(parent = '', index = 'end', iid = dolasci_count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

            dolasci_count += 1

        root_Table.update()

    except Exception as e:
        print("Error", e)

def svi_zapisi_tree_pull_db(my_tree, root_Table):
    try:    
        my_cursor.execute("SELECT osobe.Ime, dolazak.Dvorana, dolazak.Zapis, dolazak.Date FROM dolazak JOIN osobe ON osobe.ID_osobe = dolazak.ID_osobe UNION SELECT osobe.Ime, Odlazak.Dvorana, Odlazak.Zapis, Odlazak.Date FROM Odlazak JOIN osobe ON osobe.ID_osobe = Odlazak.ID_osobe ORDER BY Date DESC")
        records = my_cursor.fetchall()
        dolasci_count = 0

        for record in records:
            if dolasci_count % 2 == 0:
                my_tree.insert(parent = '', index = 'end', iid = dolasci_count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
            else:
                my_tree.insert(parent = '', index = 'end', iid = dolasci_count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

            dolasci_count += 1

        root_Table.update()

    except Exception as e:
        print("Error", e)

def remove_one_data(Id_Entry_save):
    my_cursor.execute("DELETE from lica WHERE id=" + Id_Entry_save)
    my_conn.commit()

def remove_many_data(testbroj):
    my_cursor.execute("DELETE FROM lica WHERE id=" + testbroj)
    my_conn.commit()

def remove_all_data():
    my_cursor.execute("DELETE from lica")
    my_conn.commit()

def search_records_data(my_tree, root_Table, lookup_record):   
    print(lookup_record)

    try:
        my_cursor =my_conn.cursor()
        my_cursor.execute("SELECT * FROM lica WHERE date like '%" + lookup_record + "%'")
        records = my_cursor.fetchall()
                    
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent = '', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2]), tags = ('evenrow',))
            else:
                my_tree.insert(parent = '', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2]), tags = ('oddrow',))

            count += 1

        root_Table.update()

    except Exception as e:
        print("Error", e)

def dolasci_search_records_data(my_tree, root_Table, lookup_record_ime, lookup_record_dvorana, lookup_record_date, odabir_dvorana):   
    if lookup_record_ime != "":
        try:
            my_cursor =my_conn.cursor()
            my_cursor.execute("SELECT osobe.Ime, dolazak.Dvorana, dolazak.Zapis, dolazak.Date FROM dolazak JOIN osobe ON dolazak.ID_osobe = osobe.ID_osobe WHERE Ime like '%" + lookup_record_ime + "%' AND Dvorana like '%" + odabir_dvorana + "%' ORDER BY Date DESC")
            records = my_cursor.fetchall()
                        
            count_lookup_record_ime = 0

            for record in records:
                if count_lookup_record_ime % 2 == 0:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_ime, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
                else:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_ime, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

                count_lookup_record_ime += 1

            root_Table.update()

        except Exception as e:
            print("Error", e)
    
    if lookup_record_dvorana != "":
        try:
            my_cursor =my_conn.cursor()
            my_cursor.execute("SELECT osobe.Ime, dolazak.Dvorana, dolazak.Zapis, dolazak.Date FROM dolazak JOIN osobe ON dolazak.ID_osobe = osobe.ID_osobe WHERE Dvorana like '%" + lookup_record_dvorana + "%' AND Dvorana like '%" + odabir_dvorana + "%' ORDER BY Date DESC")
            records = my_cursor.fetchall()
                        
            count_lookup_record_dvorana = 0

            for record in records:
                if count_lookup_record_dvorana % 2 == 0:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_dvorana, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
                else:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_dvorana, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

                count_lookup_record_dvorana += 1

            root_Table.update()

        except Exception as e:
            print("Error", e)

    if lookup_record_date != "":
        try:
            my_cursor =my_conn.cursor()
            my_cursor.execute("SELECT osobe.Ime, dolazak.Dvorana, dolazak.Zapis, dolazak.Date FROM dolazak JOIN osobe ON dolazak.ID_osobe = osobe.ID_osobe WHERE Date like '%" + lookup_record_date + "%' AND Dvorana like '%" + odabir_dvorana + "%' ORDER BY Date DESC")
            records = my_cursor.fetchall()
                        
            count_lookup_record_date = 0

            for record in records:
                if count_lookup_record_date % 2 == 0:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_date, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
                else:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_date, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

                count_lookup_record_date += 1

            root_Table.update()

        except Exception as e:
            print("Error", e)

    if lookup_record_ime == "" and lookup_record_dvorana == "" and lookup_record_date == "":
        try:   
            my_cursor =my_conn.cursor() 
            my_cursor.execute("SELECT osobe.Ime, dolazak.Dvorana, dolazak.Zapis, dolazak.Date FROM dolazak JOIN osobe ON dolazak.ID_osobe = osobe.ID_osobe WHERE Dvorana like '%" + odabir_dvorana + "%' ORDER BY Date DESC")
            records = my_cursor.fetchall()
            dolasci_count = 0

            for record in records:
                if dolasci_count % 2 == 0:
                    my_tree.insert(parent = '', index = 'end', iid = dolasci_count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
                else:
                    my_tree.insert(parent = '', index = 'end', iid = dolasci_count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

                dolasci_count += 1

            root_Table.update()

        except Exception as e:
            print("Error", e)

def odlasci_search_records_data(my_tree, root_Table, lookup_record_ime, lookup_record_dvorana, lookup_record_date, odabir_dvorana):   
    if lookup_record_ime != "":
        try:
            my_cursor =my_conn.cursor()
            my_cursor.execute("SELECT osobe.Ime, Odlazak.Dvorana, Odlazak.Zapis, Odlazak.Date FROM Odlazak JOIN osobe ON Odlazak.ID_osobe = osobe.ID_osobe WHERE Ime like '%" + lookup_record_ime + "%' AND Dvorana like '%" + odabir_dvorana + "%' ORDER BY Date DESC")
            records = my_cursor.fetchall()
                        
            count_lookup_record_ime = 0

            for record in records:
                if count_lookup_record_ime % 2 == 0:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_ime, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
                else:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_ime, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

                count_lookup_record_ime += 1

            root_Table.update()

        except Exception as e:
            print("Error", e)
    
    if lookup_record_dvorana != "":
        try:
            my_cursor =my_conn.cursor()
            my_cursor.execute("SELECT osobe.Ime, Odlazak.Dvorana, Odlazak.Zapis, Odlazak.Date FROM Odlazak JOIN osobe ON Odlazak.ID_osobe = osobe.ID_osobe WHERE Dvorana like '%" + lookup_record_dvorana + "%' AND Dvorana like '%" + odabir_dvorana + "%' ORDER BY Date DESC")
            records = my_cursor.fetchall()
                        
            count_lookup_record_dvorana = 0

            for record in records:
                if count_lookup_record_dvorana % 2 == 0:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_dvorana, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
                else:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_dvorana, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

                count_lookup_record_dvorana += 1

            root_Table.update()

        except Exception as e:
            print("Error", e)

    if lookup_record_date != "":
        try:
            my_cursor =my_conn.cursor()
            my_cursor.execute("SELECT osobe.Ime, Odlazak.Dvorana, Odlazak.Zapis, Odlazak.Date FROM Odlazak JOIN osobe ON Odlazak.ID_osobe = osobe.ID_osobe WHERE Date like '%" + lookup_record_date + "%' AND Dvorana like '%" + odabir_dvorana + "%' ORDER BY Date DESC")
            records = my_cursor.fetchall()
                        
            count_lookup_record_date = 0

            for record in records:
                if count_lookup_record_date % 2 == 0:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_date, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
                else:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_date, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

                count_lookup_record_date += 1

            root_Table.update()

        except Exception as e:
            print("Error", e)

    if lookup_record_ime == "" and lookup_record_dvorana == "" and lookup_record_date == "":
        try:   
            my_cursor =my_conn.cursor() 
            my_cursor.execute("SELECT osobe.Ime, Odlazak.Dvorana, Odlazak.Zapis, Odlazak.Date FROM Odlazak JOIN osobe ON Odlazak.ID_osobe = osobe.ID_osobe WHERE Dvorana like '%" + odabir_dvorana + "%' ORDER BY Date DESC")
            records = my_cursor.fetchall()
            dolasci_count = 0

            for record in records:
                if dolasci_count % 2 == 0:
                    my_tree.insert(parent = '', index = 'end', iid = dolasci_count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
                else:
                    my_tree.insert(parent = '', index = 'end', iid = dolasci_count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

                dolasci_count += 1

            root_Table.update()

        except Exception as e:
            print("Error", e)

def svi_zapisi_search_records_data(my_tree, root_Table, lookup_record_ime, lookup_record_dvorana, lookup_record_date, lookup_record_zapis):   
    if lookup_record_ime != "":
        try:
            my_cursor =my_conn.cursor()
            my_cursor.execute("SELECT osobe.Ime, dolazak.Dvorana, dolazak.Zapis, dolazak.Date FROM dolazak JOIN osobe ON osobe.ID_osobe = dolazak.ID_osobe WHERE Ime LIKE '%" + lookup_record_ime + "%' UNION SELECT osobe.Ime, Odlazak.Dvorana, Odlazak.Zapis, Odlazak.Date FROM Odlazak JOIN osobe ON osobe.ID_osobe = Odlazak.ID_osobe WHERE Ime LIKE '%" + lookup_record_ime + "%' ORDER BY Date DESC;")
            records = my_cursor.fetchall()
                        
            count_lookup_record_ime = 0

            for record in records:
                if count_lookup_record_ime % 2 == 0:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_ime, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
                else:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_ime, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

                count_lookup_record_ime += 1

            root_Table.update()

        except Exception as e:
            print("Error", e)
    
    if lookup_record_dvorana != "":
        try:
            my_cursor =my_conn.cursor()
            my_cursor.execute("SELECT osobe.Ime, dolazak.Dvorana, dolazak.Zapis, dolazak.Date FROM dolazak JOIN osobe ON osobe.ID_osobe = dolazak.ID_osobe WHERE dolazak.Dvorana LIKE '%" + lookup_record_dvorana + "%' UNION SELECT osobe.Ime, Odlazak.Dvorana, Odlazak.Zapis, Odlazak.Date FROM Odlazak JOIN osobe ON osobe.ID_osobe = Odlazak.ID_osobe WHERE Odlazak.Dvorana LIKE '%" + lookup_record_dvorana + "%' ORDER BY Date DESC;")
            records = my_cursor.fetchall()
                        
            count_lookup_record_dvorana = 0

            for record in records:
                if count_lookup_record_dvorana % 2 == 0:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_dvorana, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
                else:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_dvorana, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

                count_lookup_record_dvorana += 1

            root_Table.update()

        except Exception as e:
                print("Error", e)

    if lookup_record_zapis != "":
            try:
                my_cursor =my_conn.cursor()
                my_cursor.execute("SELECT osobe.Ime, dolazak.Dvorana, dolazak.Zapis, dolazak.Date FROM dolazak JOIN osobe ON osobe.ID_osobe = dolazak.ID_osobe WHERE dolazak.Zapis LIKE '%" + lookup_record_zapis + "%' UNION SELECT osobe.Ime, Odlazak.Dvorana, Odlazak.Zapis, Odlazak.Date FROM Odlazak JOIN osobe ON osobe.ID_osobe = Odlazak.ID_osobe WHERE Odlazak.Zapis LIKE '%" + lookup_record_zapis + "%' ORDER BY Date DESC;")
                records = my_cursor.fetchall()
                            
                count_lookup_record_zapis = 0

                for record in records:
                    if count_lookup_record_zapis % 2 == 0:
                        my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_zapis, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
                    else:
                        my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_zapis, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

                    count_lookup_record_zapis += 1

                root_Table.update()

            except Exception as e:
                print("Error", e)

    if lookup_record_date != "":
        try:
            my_cursor =my_conn.cursor()
            my_cursor.execute("SELECT osobe.Ime, dolazak.Dvorana, dolazak.Zapis, dolazak.Date FROM dolazak JOIN osobe ON osobe.ID_osobe = dolazak.ID_osobe WHERE dolazak.Date LIKE '%" + lookup_record_date + "%' UNION SELECT osobe.Ime, Odlazak.Dvorana, Odlazak.Zapis, Odlazak.Date FROM Odlazak JOIN osobe ON osobe.ID_osobe = Odlazak.ID_osobe WHERE Odlazak.Date LIKE '%" + lookup_record_date + "%' ORDER BY Date DESC;")
            records = my_cursor.fetchall()
                        
            count_lookup_record_date = 0

            for record in records:
                if count_lookup_record_date % 2 == 0:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_date, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
                else:
                    my_tree.insert(parent = '', index = 'end', iid = count_lookup_record_date, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

                count_lookup_record_date += 1

            root_Table.update()

        except Exception as e:
            print("Error", e)

    if lookup_record_ime == "" and lookup_record_dvorana == "" and lookup_record_date == "" and lookup_record_zapis == "":
        try:   
            my_cursor =my_conn.cursor() 
            my_cursor.execute("SELECT osobe.Ime, dolazak.Dvorana, dolazak.Zapis, dolazak.Date FROM dolazak JOIN osobe ON osobe.ID_osobe = dolazak.ID_osobe UNION SELECT osobe.Ime, Odlazak.Dvorana, Odlazak.Zapis, Odlazak.Date FROM Odlazak JOIN osobe ON osobe.ID_osobe = Odlazak.ID_osobe ORDER BY Date DESC;")
            records = my_cursor.fetchall()
            dolasci_count = 0

            for record in records:
                if dolasci_count % 2 == 0:
                    my_tree.insert(parent = '', index = 'end', iid = dolasci_count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
                else:
                    my_tree.insert(parent = '', index = 'end', iid = dolasci_count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))

                dolasci_count += 1

            root_Table.update()

        except Exception as e:
            print("Error", e)