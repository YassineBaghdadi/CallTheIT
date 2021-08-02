import getpass
import platform
import socket, os
import subprocess
import sys

from requests import get
from win10toast import ToastNotifier
from PyQt5 import QtWidgets, uic

hosts = ['10.73.100.101', '10.73.1.115', '10.73.2.68']
port = 1233


class Main(QtWidgets.QWidget):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi("c.ui", self)
        self.yassine, self.anass, self.karzazi = None, None, None
        for i, v in enumerate(hosts):
            if i == 0:
                self.yassine = subprocess.call(['ping', '-n' if platform.system().lower()=='windows' else '-c', '1', v]) == 0
            elif i == 1:
                self.anass = subprocess.call(['ping', '-n' if platform.system().lower()=='windows' else '-c', '1', v]) == 0
            elif i == 2:
                self.karzazi = subprocess.call(['ping', '-n' if platform.system().lower()=='windows' else '-c', '1', v]) == 0

        self.YB.setEnabled(self.yassine)
        self.AK.setEnabled(self.anass)
        self.MK.setEnabled(self.karzazi)

        self.YB.clicked.connect(lambda : self.call(hosts[0], 'Yassine Baghdadi'))
        self.AK.clicked.connect(lambda : self.call(hosts[1], 'Anass Kada '))
        self.MK.clicked.connect(lambda : self.call(hosts[2], 'Mohammed Karzazi'))



        self.show()

    def call(self, host, name):
        ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ip = get('https://api.ipify.org').text

        text = f"""
            + User Name : {getpass.getuser()}\n+ Host Name : {socket.gethostname()}\n+ Local IP : {socket.gethostbyname(socket.gethostname())}\n{f"+ Message : {self.txt.text()}" if len(self.txt.text())>0 else ""}
        """

        try:
            ClientSocket.connect((host, port))
        except socket.error as e:
            print(str(e))
            toast = ToastNotifier()
            toast.show_toast(f"Error : Can't Connect to {name}", f'{e}', duration=15, icon_path="it.ico")
        try:
            ClientSocket.send(str.encode(text))
            self.txt.clear()
        except OSError as e:
            print(e)
            toast = ToastNotifier()
            toast.show_toast("Err", f'Can\'t reach {name} in the moment ',
                             duration=10, icon_path="it.ico")

        ClientSocket.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())

