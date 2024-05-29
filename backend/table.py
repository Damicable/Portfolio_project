import mysql.connector


connection = mysql.connector.connect(
    host= 'localhost',
    user= 'cuisine_dev',
    passwd= '2024**',
    database= 'cuisine_dev_db'
)

cursor = connection.cursor()

cursor.execute('SHOW TABLES')

tables = cursor.fetchall()
for table in tables:
    print(table[0])


cursor.close()
connection.close()