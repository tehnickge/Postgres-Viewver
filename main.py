from tkinter import *
from tkinter.ttk import *
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import timedelta, datetime
import psycopg2
from psycopg2 import Error
import json
with open('config.json', 'r', encoding='utf-8') as f: #открыли файл с данными
    text = json.load(f) 

def get_name_db():
    name_db = switchbox1.get()
    return name_db
    
def get_name_table():
    name_table = switchbox2.get()
    return name_table

def try_to_get_all_table_coontection_in_db():
    name_db = get_name_db()
    column_in_db = []
    try:
        connection = psycopg2.connect(user=text['userName'],
                                  password=text['password'],
                                  host=text['host'],
                                  port=text['port'],
                                  database=name_db)
        cursor = connection.cursor()
        #SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';
        query="""SELECT table_name
  FROM information_schema.tables
 WHERE table_schema='public'
   AND table_type='BASE TABLE';"""
        item_tuple =()
        cursor.execute(query,item_tuple)
        
        connection.commit()
        record = cursor.fetchall()
        print("***\n\n")
        for i in record:
            for a in i:
                column_in_db.append(a)
        print(column_in_db[0] + "<<< ")
        print("***\n\n")
        print("Вы подключены к - ", record, "\n")
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
    return column_in_db

def get():
    switchbox2['values'] = ()
    print(db_name.get())
    all_colums = try_to_get_all_table_coontection_in_db()
    switchbox2['values'] = all_colums
    label1['text'] = (select_request + get_name_db())

def select_to_bd():
    name_db = get_name_db()
    table_name = get_name_table()
    array_res = []
    try:
        connection = psycopg2.connect(user=text['userName'],
                                  password=text['password'],
                                  host=text['host'],
                                  port=text['port'],
                                  database=name_db)
        cursor = connection.cursor()
        #SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';
        query="SELECT * FROM " + table_name
        item_tuple =()
        
        cursor.execute(query,item_tuple)
        
        connection.commit()
        print("*********\n*********\n*********")
        for i in range(0,25):
            record = cursor.fetchone()
            array_res.append(record)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
            return array_res
        
def require_to_bd(require_str):
    name_db = get_name_db()
    name_table = switchbox2.get()
    array_res = []
    try:
        connection = psycopg2.connect(user=text['userName'],
                                  password=text['password'],
                                  host=text['host'],
                                  port=text['port'],
                                  database=name_db)
        cursor = connection.cursor()
        #SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';
        query=require_str
        item_tuple =()
        
        cursor.execute(query)
        
        connection.commit()
        print("*********\n*********\n*********")
        for i in range(0,25):
            record = cursor.fetchone()
            array_res.append(record)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
            return array_res

def get_info_to_table():
    table.delete(*table.get_children())
    array_data = select_to_bd()
    print('_________________________')
    print(array_data)
    for i in array_data:
        table.insert('',END,values=i)

def make_select_to_bd():
    table1.delete(*table1.get_children())
    __temp__ = input1.get()
    __res__ = require_to_bd(__temp__)
    for i in __res__:
        table1.insert('',END,values=i)






win = Tk()
win.geometry("1300x1000")
win.minsize(500, 350)
win.title('test table')

frame = Frame(borderwidth=1, relief=SOLID, padding=[8,10])

###
mystring = StringVar(win)
db_name = StringVar(win)
test_array = StringVar()
array_with_data_base_names = StringVar()
select_request = "введите селект/инсерт запрос в бд from: "

##
switchbox1 = Combobox(frame,textvariable=array_with_data_base_names)
arr = []
for txt in text["nameDB"]:
    arr += txt
    
switchbox1['values'] = arr
switchbox1.pack()

button1 = Button(frame,text="get",command=get).pack()

switchbox2 = Combobox(frame,textvariable=test_array)
switchbox2.pack()

button2 = Button(frame,text="get",command=get_info_to_table).pack()

table = Treeview(frame, show="headings")
table['columns'] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
for i in range(0,16):
    table.column(i,stretch=NO, width=50)
        
table.pack()

label1 = Label(frame, text=(select_request + get_name_db()))
label1.pack()

input1 = Entry(frame)
input1.pack()

button3 = Button(frame,text="get",command=make_select_to_bd).pack()

table1 = Treeview(frame,show="headings")
table1['columns'] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
for i in range(0,16):
    table1.column(i,stretch=NO, width=50)
    
scrollbar = Scrollbar(frame,command=table1.yview())
table1.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
table1.pack(expand=YES,fill=BOTH)




frame.pack(padx=20,pady=20)
##
win.mainloop()