import socket
from _thread import *
import sys

server = "192.168.0.27"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(4)
print("Waiting for connection")

def read_pos(str):
    print(str)
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    res = ""
    for item in tup:
        print(item)
        res += str(item[0]) + ","
        res += str(item[1]) + ","
    print(res[0:-1])
    return res[0:-1]

pos = [(0, 0), (100, 100), (200, 200), (300, 300)]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode("utf-8"))
            pos[player] = data
            
            if not data:
                print("Disconnected")
                break
            else:
                #print(player)
                if player == 0:
                    reply = (pos[1], pos[2], pos[3])
                elif player == 1:
                    reply = (pos[0], pos[2], pos[3])
                elif player == 2:
                    reply = (pos[0], pos[1], pos[3])
                else:
                    reply = (pos[0], pos[1], pos[2])
               
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break
    
    print("Connection lost")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
