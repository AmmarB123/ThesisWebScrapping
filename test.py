"""
This class is not mentioned in my report because it is just a tester to check if the stored data is getting deleted
"""

import sqlite3
conn = sqlite3.connect('userdata.db')
cursor = conn.cursor()
username = "2e2cd55131777f930f9941c2d4f111fe0acb00de99a3c1852de2843f7831a9bf"

cursor.execute("SELECT rowid FROM userdata WHERE username = ?", (username,))
result = cursor.fetchone()

if result is not None:
    # Retrieve the primary key value
    primary_key = result[0]
    print(primary_key)
    print("Primary key for user", username, "is", primary_key)
else:
    print("User", username, "not found")

cursor.execute("SELECT Website, Title, Price, Stock, Rating, Review, Description, Color, Size, Link FROM items WHERE user_id=?", (primary_key,))
items = cursor.fetchall()
print("Items for user with ID {}: {}".format(primary_key, len(items)))



