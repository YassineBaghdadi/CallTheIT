import socket, os, sys

from win10toast import ToastNotifier

ClientSocket = socket.socket()
hosts = ['10.73.100.101', '10.73.100.100']
port = 1233

def call(host):
    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))
    try:
        ClientSocket.send(str.encode(f"{os.getlogin()} need the IT GUYS in : {socket.gethostname()}/{socket.gethostbyname(socket.gethostname())}"))
    except OSError :
        toast = ToastNotifier()
        toast.show_toast("Alert", f'Can\'t reach {"YASSINE" if host == host[0] else "ANASS"} in the moment ', duration=10, icon_path="it.ico")

    ClientSocket.close()

[call(i) for i in hosts]

exit()
