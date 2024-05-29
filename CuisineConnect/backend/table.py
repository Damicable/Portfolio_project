import mysql.connector


connection = mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    passwd= 'Mi94ch12ae07l',
    database= 'cuisine_dev_db2'
)

cursor = connection.cursor()

cursor.execute('SHOW TABLES')

tables = cursor.fetchall()
for table in tables:
    print(table[0])


cursor.close()
connection.close()