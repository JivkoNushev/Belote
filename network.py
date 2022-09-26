import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.27"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = self.connect()

    def getPlayer(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048 * 10000).decode() 
        except:
            pass
    
    def send(self, command):
        try:
            self.client.send(str.encode(command))
            return pickle.loads(self.client.recv(2048 * 10000))
        except socket.error as e:
            print(e)