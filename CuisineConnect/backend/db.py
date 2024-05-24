from flask_sqlalchemy import SQLAlchemy
import mysql.connector

mydb = mysql.connector.connect(
    host= 'localhost',
    user = 'root',
    passwd= 'pwd@2024**',
)

my_cursor = mydb.cursor()

my_cursor.execute('CREATE DATABASE cuisine_dev_db')

my_cursor.execute('SHOW DATABASES')
for db in my_cursor:
    print(db)