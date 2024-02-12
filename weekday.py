import sqlite3
# Establish a connection to the database
connect = sqlite3.connect("weekday.db")
# Create a cursor object to execute SQL queries
cur = connect.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS WEEKDAY
         (ID INT PRIMARY KEY NOT NULL,
         weekday TEXT NOT NULL);''')