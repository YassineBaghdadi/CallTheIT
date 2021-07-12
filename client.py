import getpass
import socket, os
from requests import get
from win10toast import ToastNotifier


hosts = ['10.73.100.101', '10.73.1.115']
port = 1233

def call(host):
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = get('https://api.ipify.org').text
    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))
    try:
        ClientSocket.send(str.encode(
            f"UserName : {getpass.getuser()}\nHostName : {socket.gethostname()}\nLocal IP : {socket.gethostbyname(socket.gethostname())}\nPublic IP : {ip}"))
    except OSError:
        toast = ToastNotifier()
        toast.show_toast("Alert", f'Can\'t reach {"YASSINE" if host == hosts[0] else "ANASS"} in the moment ',
                         duration=10, icon_path="it.ico")

    ClientSocket.close()


[call(i) for i in hosts]

exit()
