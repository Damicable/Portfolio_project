import mysql.connector

mydb = mysql.connector.connect(
    host= 'localhost',
    user = 'root',
    passwd= '2024**',
)

my_cursor = mydb.cursor()

my_cursor.execute('CREATE DATABASE cuisineconnect_dev_db')

my_cursor.execute('SHOW DATABASES')
for db in my_cursor:
    print(db)
