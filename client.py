import getpass
import platform
import socket, os,  subprocess, sys, pymysql

from requests import get
from win10toast import ToastNotifier
from PyQt5 import QtWidgets, uic
with open('ips.txt', 'r') as f:
    hosts = f.readlines()
port = 1233

def con():
    return pymysql.connect(host="127.0.0.1", user='test', password='test', database="CallTheIT", port=3306)


class GetName(QtWidgets.QWidget):
    def __init__(self):
        super(GetName, self).__init__()
        uic.loadUi("getName.ui", self)

        self.save.clicked.connect(self.save_)

    def save_(self):
        conn = con()
        curs = conn.cursor()
        curs.execute(f"""insert into Agents(name, ip, hostname) values("{self.name.text()}", "{socket.gethostbyname(socket.gethostname())}", "{socket.gethostname()}")""")
        conn.commit()
        conn.close()
        main = Main()
        main.show()
        self.close()




class Main(QtWidgets.QWidget):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi("c.ui", self)
        ips = []
        conn = con()
        curs = conn.cursor()
        curs.execute("create table if not exists Agents(id INT AUTO_INCREMENT PRIMARY KEY, name Varchar(50), ip varchar(20), hostname Varchar(50));")
        curs.execute("""create table if not exists history(
            id INT AUTO_INCREMENT PRIMARY KEY,
             time Varchar(50),
              agentId int,
                 message text,
                  status varchar(20),
                  it varchar(50),
                  FOREIGN KEY (agentId) REFERENCES Agents(id));""")

        conn.commit()
        curs.execute(f"select id from Agents where ip like '{socket.gethostbyname(socket.gethostname())}'")
        agentId = curs.fetchone()[0]
        if  agentId:
            self.agentId = int(agentId)
        else :
            self.close()
            getname = GetName()
            getname.show()
        conn.close()
        for i, v in enumerate(hosts):
            v = v.replace('\n', '')
            ips.append(subprocess.call(['ping', '-n' if platform.system().lower()=='windows' else '-c', '1', v]) == 0)


        self.YB.setEnabled(ips[0])
        self.AK.setEnabled(ips[1])
        self.MK.setEnabled(ips[2])

        self.YB.clicked.connect(lambda : self.call(hosts[0], 'Yassine Baghdadi'))
        self.AK.clicked.connect(lambda : self.call(hosts[1], 'Anass Kada '))
        self.MK.clicked.connect(lambda : self.call(hosts[2], 'Mohammed Karzazi'))



        self.show()

    def call(self, host, name):
        conn = con()
        cur = conn.cursor()

        ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ip = get('https://api.ipify.org').text

        text = f"""
            + Agent Name : {self.agentName}\n+ Host Name : {socket.gethostname()}\n+ Local IP : {socket.gethostbyname(socket.gethostname())}\n{f"+ Message : {self.txt.text()}" if len(self.txt.text())>0 else ""}
        """
        current_time = None

        self.status = None
        try:
            ClientSocket.connect((host, port))
        except socket.error as e:
            print(str(e))
            toast = ToastNotifier()
            toast.show_toast(f"Error : Can't Connect to {name}", f'{e}', duration=15, icon_path="it.ico")
            self.status = 'FAILED'
        try:
            ClientSocket.send(str.encode(text))
            self.status = 'DONE'
            self.txt.clear()
        except OSError as e:
            print(e)
            toast = ToastNotifier()
            toast.show_toast("Err", f'Can\'t reach {name} in the moment ',
                             duration=10, icon_path="it.ico")
            self.status = 'FAILED'

        ClientSocket.close()
        cur.execute(query=f"insert into history (time, agentId, message, status, it) values('{current_time}', '{self.agentId}', '{self.txt.text()}', '{self.status}', '{name}')")
        conn.commit()
        conn.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())

