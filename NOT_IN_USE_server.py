'''
NOT IN USE

import sqlite3
import hashlib
import socket
import threading
#from frontend import LoginMenu
def server(username1, password1):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(("localhost", 4444))

    server.listen()

    #username1, password1 = LoginMenu.login()

    #print(username1, password1)



    def handle_connection(connect, username1, password1):
        connect.send(username1.encode())
        username = connect.recv(1024).decode()
        connect.send(password1.encode())
        password = connect.recv(1024)
        password = hashlib.sha256(password).hexdigest()

        connectsql = sqlite3.connect("userdata.db")
        current = connectsql.cursor()

        current.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

        if current.fetchall():
            connect.send("Login success".encode())
        else:
            connect.send("Login failed".encode())


    while True:
        client, add =server.accept()
        threading.Thread(target=handle_connection, args=(client, )).start()

'''