import mysql.connector
import csv
f = open("Adidas US Sales Datasets (1).csv","r")
r = csv.reader(f)
rec = []
for i in r:
    i[7] = i[7].replace("$","")
    i[9] = i[9].replace("$","")
    i[9] = i[9].replace(",","")
    i[10] = i[10].replace("$","")
    i[10] = i[10].replace(",","")
    rec.append(i)
rec = rec[1::]
for i in range(len(rec)):
    rec[i][7] = int(float(rec[i][7]))
    rec[i][8] = int(rec[i][8])
    rec[i][9] = int(rec[i][9])
    rec[i][10] = int(rec[i][10])
db = mysql.connector.connect(
    host = "database-1.c0kcbpmjblfm.ap-south-1.rds.amazonaws.com",
    user = "admin",password = "12345678",database = "sales",
    port = 3306
)
cur = db.cursor()
c = 1
for i in rec:
    # print(type(i[4]))
    # print(type(i[6]))
    # print(type(i[7]))
    # print(type(i[8]))
    # print(type(i[9]))
    # print(type(i[10]))
    val = (i[0],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[12])
    cur.execute(f"insert into salesfil values {val}")
    print(f"{c} records inserted")
    c+=1
db.commit()
print("Records inserted")
