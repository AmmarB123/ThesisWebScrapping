'''
Not in use
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 4444))

message = client.recv(1024).decode()
client.send(input(message).encode())
message = client.recv(1024).decode()
client.send(input(message).encode())

if client.recv(1024).decode() == "Login success":
    print("Time to Scrape")
else:
    print("Rerun")
#print(client.recv(1024).decode())
'''
