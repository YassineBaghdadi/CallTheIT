import datetime
import getpass
import platform
import socket, os,  subprocess, sys, pymysql

from requests import get
from win10toast import ToastNotifier
from PyQt5 import QtWidgets, uic
with open('ips.txt', 'r') as f:
    hosts = [i.replace('\n', '') for i in f.readlines()]
port = 1233



def con():
    return pymysql.connect(host=hosts[0], user='test', password='test', database="CallTheIT", port=3306)


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
        self.main = Main()
        self.main.show()
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
        curs.execute(f"select id, name from Agents where ip like '{socket.gethostbyname(socket.gethostname())}'")
        self.agent = curs.fetchone()
        print(self.agent)
        if self.agent is not None:
            self.agentId = self.agent[0]
            self.show()
        else :
            self.close()
            self.getname = GetName()
            self.getname.show()


        conn.close()
        for i, v in enumerate(hosts):
            v = v.replace('\n', '')
            ips.append(subprocess.call(['ping', '-n' if platform.system().lower()=='windows' else '-c', '1', v]) == 0)


        self.YB.setEnabled(ips[0])


        self.YB.clicked.connect(lambda : self.call(hosts[0], 'Yassine Baghdadi'))






    def call(self, host, name):
        conn = con()
        cur = conn.cursor()

        ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ip = get('https://api.ipify.org').text

        text = f"""
            + Agent Name : {self.agent[1]}\n+ Host Name : {socket.gethostname()}\n+ Local IP : {socket.gethostbyname(socket.gethostname())}\n{f"+ Message : {self.txt.text()}" if len(self.txt.text())>0 else ""}
        """
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

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
            toast = ToastNotifier()
            toast.show_toast("Request Sent : ", f'The Request sent successfully to {name} \nhe\'ll be here within a moment .',
                             duration=20, icon_path="it.ico")
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
        exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
