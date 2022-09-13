import socket
import pickle
from _thread import *
from player import Player 

server = "192.168.0.27"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(4)
print("Waiting for connection")

players = [Player(0,0,100,100,(0,255,0)), Player(100,100,100,100,(255,0,0)), Player(200,200,100,100,(255,0,0)), Player(300,300,100,100,(255,0,0))]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = [0,0,0,0]

    while True:
        try:
            PlayerData = pickle.loads(conn.recv(2048 * 10000))
            players[player] = PlayerData
            if not PlayerData:
                print("Disconnected")
                break
            if player == 0:
                reply[0] = players[1]
                reply[1] = players[2]
                reply[2] = players[3]
            elif player == 1:
                reply[0] = players[0]
                reply[1] = players[2]
                reply[2] = players[3]
            elif player == 2:
                reply[0] = players[1]
                reply[1] = players[0]
                reply[2] = players[3]
            else:
                reply[0] = players[1]
                reply[1] = players[2]
                reply[2] = players[0]
            print(reply[0].get_pos())

            conn.sendall(pickle.dumps(reply))
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
