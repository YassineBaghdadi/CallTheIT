import http.server, os, logging, ctypes
from datetime import datetime
from plyer import notification
def send_notification(title, message, duration=10):
    os.system(f'powershell.exe -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show(\\"{message}\\", \\"{title}\\", 0, 16)"')
logging.basicConfig(filename='access.log', level=logging.INFO)

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        #ctypes.windll.user32.MessageBoxW(None, f'{self.client_address[0]} : need help ', "Notification", 0x00001000)
        #send_notification("Notification", f'{self.client_address[0]} : need help ')
        os.system(f'notify-send "HelpDesk Saccom" "{self.client_address[0]} : need help " ')
        #os.system(f"notify-send '{self.client_address[0]} : need help '")
        logging.info(f'- {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}     IP: {self.client_address[0]}' )
        self.send_response(200)
        self.end_headers()

httpd = http.server.HTTPServer(("", 8000), MyHandler)
httpd.serve_forever()