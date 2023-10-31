import psycopg2
import numpy as np
import pandas as pd
from datetime import datetime
from tkinter import *
from tkinter.ttk import *
import time
# from PIL import Image, ImageTk

app = Tk()
app.geometry('1100x250')
app.title('Program Save DATA 2nd-Mask 2M-09')

app.iconbitmap(r'icon.ico')

my_text_status = 'Processing'
my_text1 = 'SELECT DATA TWOMASK_CPK Finish'
my_text2 = 'SELECT DATA CPK_DATA Finish'
my_text3 = 'DELETE DATA TWOMASK_CPK Finish'
my_text4 = 'DELETE DATA CPK_DATA Finish'
my_text5 = 'RESET ID DATA TWOMASK_CPK Finish'
my_text6 = 'RESET ID DATA CPK_DATA Finish'

dt = datetime.now()

ts =datetime.timestamp(dt)

date_time = datetime.fromtimestamp(ts)

times = date_time.strftime("%m %Y")

def select_twomask_cpk() :
    concon = psycopg2.connect(user="admin",password="Ab123456",host="191.191.2.197",port="5432",database="Totle-2nd-Mask")
    print("connect PostgreSQL")
    Data = concon.cursor()
    Data.execute("select * from twomask_cpk")
    concon.commit()
    dataLP = Data.fetchall()
    lp = pd.DataFrame(dataLP)
    lp.drop([0], axis=1, inplace=True)
    dataT = lp.rename(columns={1:'front_pos',2:'front_width',3:'back_pos',4:'back_width',5:'Lot',})
    dataT.to_csv(f"""DATA TWOMASK_2M-09_{times}.csv""",index=False)
    # print('data1')
    concon.close()
    global my_text1
    my_label_select_twomask.config(text = 'Status : '+my_text1)
    
def select_cpk_data() :
    concon = psycopg2.connect(user="admin",password="Ab123456",host="191.191.2.197",port="5432",database="Totle-2nd-Mask")
    print("connect PostgreSQL")
    Data = concon.cursor()
    Data.execute("select * from cpk_data")
    concon.commit()
    dataLP = Data.fetchall()
    lp = pd.DataFrame(dataLP)
    lp.drop([0], axis=1, inplace=True)
    dataCPK = lp.rename(columns={1:'front_pos',2:'front_width',3:'back_pos',4:'back_width',5:'Lot',6:'Partname',7:'times',})
    dataCPK.to_csv(f"""CPK_DATA_{times}.csv""",index=False)
    print('data2')
    concon.close()
    global my_text2
    my_label_select_cpk.config(text = 'Status : '+my_text2)


def delete_twomask_cpk():
    concon = psycopg2.connect(user='admin',password='Ab123456',host='191.191.2.197',port='5432',database='Totle-2nd-Mask')
    delete_twomask = concon.cursor()
    delete_twomask.execute('DELETE FROM twomask_cpk')
    concon.commit()
    concon.close()
    global my_text3
    my_label_delete_twomask.config(text = 'Status : '+my_text3)

def delete_cpk_data():
    concon = psycopg2.connect(user='admin',password='Ab123456',host='191.191.2.197',port='5432',database='Totle-2nd-Mask')
    delete_cpk = concon.cursor()
    delete_cpk.execute('DELETE FROM cpk_data')
    concon.commit()
    concon.close()
    global my_text4
    my_label_delete_cpk.config(text = 'Status : '+my_text4)


def reset_twomask_cpk():
    concon = psycopg2.connect(user='admin',password='Ab123456',host='191.191.2.197',port='5432',database='Totle-2nd-Mask') 
    reset_twomask = concon.cursor()
    reset_twomask.execute('TRUNCATE TABLE twomask_cpk RESTART IDENTITY;')
    concon.commit()
    concon.close()
    global my_text5
    my_label_reset_twomask.config(text = 'Status : '+my_text5)

def reset_cpk_data():
    concon = psycopg2.connect(user='admin',password='Ab123456',host='191.191.2.197',port='5432',database='Totle-2nd-Mask')
    reset_cpk = concon.cursor()
    reset_cpk.execute('TRUNCATE TABLE cpk_data RESTART IDENTITY;')
    concon.commit()
    concon.close()
    global my_text6
    my_label_reset_cpk.config(text = 'Status : '+my_text6)
    


    


#--------------------------------------------------SELECT DATA ------------------------------------------------#
select_twomask = Button(app,text='SELECT ALL DATA EXCEL',command=select_twomask_cpk)
select_twomask.grid(row = 1, column = 1,pady=50,padx=100)

select_cpk = Button(app,text='SELECT CPK_DATA',command=select_cpk_data)
select_cpk.grid(row = 2, column = 1,padx=130)

#--------------------------------------------------- DELETE DATA -----------------------------------------------#
delete_twomask = Button(app,text='DELETE TWOMASK_CPK',command=delete_twomask_cpk)
delete_twomask.grid(row = 1, column = 2,pady=50,padx=100)

delete_cpk = Button(app,text='DELETE CPK_DATA',command=delete_cpk_data)
delete_cpk.grid(row = 2, column = 2,padx=130)

#---------------------------------------------------- RESET ID DATA ----------------------------------------------#
reset_twomask = Button(app,text='RESET ID TWOMASK_CPK',command=reset_twomask_cpk)
reset_twomask.grid(row = 1, column = 3,pady=50,padx=100)

reset_cpk = Button(app,text='RESET ID CPK_DATA',command=reset_cpk_data)
reset_cpk.grid(row = 2, column = 3,padx=130)



#---------------------- LAABLE ----------------------------#

my_label_select_twomask = Label(app,
                 text = "Status :")
my_label_select_twomask.place(x = 60, y = 180) 

my_label_select_cpk = Label(app,
                 text = "Status:")
my_label_select_cpk.place(x = 60, y = 200) 

#--------------------------------------------------#

my_label_delete_twomask = Label(app,
                 text = "Status : ")
my_label_delete_twomask.place(x = 440, y = 180) 

my_label_delete_cpk = Label(app,
                 text = "Status : ")
my_label_delete_cpk.place(x = 440, y = 200) 

#--------------------------------------------------#

my_label_reset_twomask = Label(app,
                 text = "Status : ")
my_label_reset_twomask.place(x = 800, y = 180) 

my_label_reset_cpk = Label(app,
                 text = "Status : ")
my_label_reset_cpk.place(x = 800, y = 200) 

#--------------------------------------------------#
app.mainloop()