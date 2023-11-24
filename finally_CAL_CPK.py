import pandas as pd
import numpy as np
import psycopg2
from datetime import datetime
import time

#-----------------------------------SELECT DATABASE ---------------------------------#

connection = psycopg2.connect(user="admin",
                              password="Ab123456",
                              host="10.53.8.7",
                              port="5432",
                              database="Totle-2nd-Mask")
print("connect PostgreSQL")

#------------------------- select Database to lot_partname---------------------------#

Data_Lot_Partname = connection.cursor()
Data_Lot_Partname.execute("select * from lot_partname;")
connection.commit()
dataLP = Data_Lot_Partname.fetchall()

lp = pd.DataFrame(dataLP)

lp.drop([0], axis=1, inplace=True)

lp.to_csv("data.csv",index=False)

LP = pd.read_csv("data.csv",index_col=False)

LP.reset_index(drop=True)

# LP['1'] is colunm name นับเป็น index column ที่ 0 1 2 ...
x = LP['1']
X = np.array(x)
Lot = X[0]
# print(Lot)

y = LP['2']
Y = np.array(y)
Partname = Y[0]
# print(Partname)

#-------------------------------------------------------------------------------------#


#----------------------------select Database to twomask_cpk----------------------------#

Data_twomask_cpk = connection.cursor()

Data_twomask_cpk.execute("select * from twomask_cpk;")

connection.commit()

records = Data_twomask_cpk.fetchall()

df = pd.DataFrame(records)

df.drop([0], axis=1, inplace=True)

df.to_csv("twomask_CPK.csv",index=False)

rd = pd.read_csv("twomask_CPK.csv",index_col=False)

rd = rd.loc[rd['5'] == Lot]
# data_T = rd

dataT = rd.rename(columns={'1':'front_pos','2':'front_width','3':'back_pos','4':'back_width','5':'Lot'})
# print(rd['1'])
dataT.to_csv(f"""twomask_CPK_{Lot}_{Partname}.csv""",index=False)

#---------------------------------------------------------------------------------------#

#-------------------------------- USL-LSL DATA -----------------------------------------#

ul = pd.read_csv("spec_2m.csv",index_col=False)
ul.reset_index(drop=True)
ul = ul.loc[ul['Partname'] == Partname]

x1 = ul['min_P']
x2 = ul['max_P']
x3 = ul['min_W']
x4 = ul['max_W']
x5 = ul['Partname']

X11 = np.array(x1)
X12 = np.array(x2)
X13 = np.array(x3)
X14 = np.array(x4)
X15 = np.array(x5)

min_P = X11[0]
max_P = X12[0]
min_W = X13[0]
max_W = X14[0]
PartnameTB = X15[0]

LSL_P = min_P
USL_P = max_P

LSL_W = min_W
USL_W = max_W

#---------------------------------------------------------------------------------------#

#------------------------------------ Calculate CPK ------------------------------------# 
def Cpk(mylist, usl, lsl):
        arr = np.array(mylist)
        arr = arr.astype(np.float64)
        arr = arr[~np.isnan(arr)]
        arr = arr.ravel()
        sigma = np.std(arr)
        m = np.mean(arr)
        # print('arr',usl)
        print('arr',arr)
        Cpu = float(usl - m) / (3 * sigma)
        Cpl = float(m - lsl) / (3 * sigma)
        Cpk = np.min([Cpu, Cpl])
        return Cpk

Cpk_front_pos = Cpk(rd["1"],USL_P,LSL_P)
Cpk_front_width = Cpk(rd["2"],USL_W,LSL_W)
Cpk_back_pos = Cpk(rd["3"],USL_P,LSL_P)
Cpk_back_width = Cpk(rd["4"],USL_W,LSL_W)

datacpk_front_pos = '%.3f'%(Cpk_front_pos)
datacpk_front_width = '%.3f'%(Cpk_front_width)
datacpk_back_pos = '%.3f'%(Cpk_back_pos)
datacpk_back_width = '%.3f'%(Cpk_back_width)


# print(datacpk_front_pos)
# print(datacpk_front_width)
# print(datacpk_back_pos)
# print(datacpk_back_width)
print(Lot)
print(Partname)
# print(times)

#--------------------------------------------------------------------------------------#

dt = datetime.now()

ts =datetime.timestamp(dt)

date_time = datetime.fromtimestamp(ts)

times = date_time.strftime("%d-%m-%Y  %H:%M:%S")

# print("date and time is :",dt)
# print("Result 1:", times)
# print(Lot)
# print(Partname)
#--------------------------------------------------------------------------------------#

#----------------------------------- INSERT TO DATABASE -------------------------------#
con = connection.cursor()

a = "INSERT INTO cpk_data(cpk_front_pos, cpk_front_width,cpk_back_pos, cpk_back_width, lot, partname, times) VALUES (%s, %s, %s, %s, %s, %s, %s)"
b = (datacpk_front_pos, datacpk_front_width, datacpk_back_pos, datacpk_front_width, Lot, Partname, times)

empty_array = datacpk_front_pos

# Check Blank value from front pos
def is_empty_with_operation_not():
    if empty_array:
        print('INSERT ')
        con.execute(a,b)
        connection.commit()
        return True
    return False

sta = time.time()
id_empty = is_empty_with_operation_not()
sto = time.time()
print("11%.8f sec."%(sto - sta))
connection.close()

print("INSERT INTO SUBMIT MY DATABASE PG ADMIN")

# #----------------------------------------------------------------------------------------#
