import mysql.connector
database = mysql.connector.connect(host = "database-1.clrbethb6kqw.ap-south-1.rds.amazonaws.com",
                                    username = "root",password="12345678",port=3306,database="emp")

cursor = database.cursor()

# cursor.execute(f"insert into addtask(emp_id,task,compornot,tod_date) values({10001},'sleep',{False},'2023-08-19')")
# database.commit()