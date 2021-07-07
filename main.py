
import socket
import os
from _thread import *
from win10toast import ToastNotifier

ServerSocket = socket.socket()
host = '0.0.0.0'
port = 1233
ThreadCount = 0
toast = ToastNotifier()

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    toast.show_toast("ERROR : ", f"{str(e)}", duration=10, icon_path="it.ico")
    print(str(e))
    exit()

ServerSocket.listen(5)


def threaded_client(connection):
    while True:
        data = connection.recv(1024)
        toast.show_toast("Some one needs The IT GUYS", data.decode('utf-8'), duration=20, icon_path="it.ico")
        print(data.decode('utf-8'))
        if not data:
            break
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1

ServerSocket.close()
