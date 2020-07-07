import mysql.connector
import datetime

database_name='big'
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database=database_name,
auth_plugin='mysql_native_password'
)
table='matches2'
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE "+table+" (id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,date DATE,time VARCHAR(255),teams VARCHAR(255))")



# mycursor.execute("delete from matches where id>0")
# mycursor.execute("ALTER TABLE matches AUTO_INCREMENT=1")
mydb.commit()
mydb.close()
print("done")
exit()
