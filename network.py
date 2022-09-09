import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.IF_INET, socket.SOCK_STREAM)