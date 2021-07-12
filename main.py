
import socket
import os
from _thread import *
from win10toast import ToastNotifier

import winsound


def make_noise():
    duration = 1000  # milliseconds
    freq = 800  # Hz
    winsound.Beep(freq, duration)


ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = '0.0.0.0'
port = 1233
ThreadCount = 0
toast = ToastNotifier()

try:
    ServerSocket.bind((host, port))
    ServerSocket.listen(30)
except socket.error as e:
    toast.show_toast("ERROR : ", f"{str(e)}", duration=10, icon_path="it.ico")
    print(str(e))
    exit()

ServerSocket.listen(5)


def threaded_client(connection):
    while True:
        data = connection.recv(1024)
        toast.show_toast("Some one needs The IT GUYS : ", data.decode('utf-8'), duration=86400, icon_path="it.ico")
        make_noise()
        print(data.decode('utf-8'))
        if not data:
            break
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1

ServerSocket.close()
