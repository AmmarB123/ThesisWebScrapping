import sqlite3
# Establish a connection to the database
connect = sqlite3.connect("userdata.db")
# Create a cursor object to execute SQL queries
cur = connect.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata(
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    word VARCHAR(255) NOT NULL
)
""")

cur.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        Website TEXT,
        Title TEXT,
        Price TEXT,
        Stock TEXT,
        Rating TEXT,
        Review TEXT,
        Description TEXT,
        Color TEXT,
        Size TEXT,
        Link TEXT,
        FOREIGN KEY (user_id) REFERENCES userdata(id)
    )
''')