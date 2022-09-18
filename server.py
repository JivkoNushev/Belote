import socket
import pickle
from _thread import *
from sqlite3 import connect
from player import Player 
from game import Game

server = "192.168.0.27"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen() # needs to be tested with/without parameters
print("Waiting for connection")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, player, gameId):
    global idCount
    conn.send(str.encode(str(player)))

    reply = ""
    while True:
        try:
            data = conn.recv(2048 * 10000).decode()
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    reply = game
                    if data == "reset":
                        reply.reset_moves()
                    elif data != "get":
                        reply.make_move(player, data)
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game:", gameId)
    except:
        pass

    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1
    gameId = (idCount - 1) // 4
    player = (idCount - 1) % 4

    if idCount % 4 == 1:
        games[gameId] = Game(gameId)
        print("Starting a new game")
    elif idCount % 4 == 0:
        games[gameId].ready = True

    start_new_thread(threaded_client, (conn, player, gameId))
