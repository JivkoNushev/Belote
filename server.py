import socket
import pickle
from _thread import *
from sqlite3 import connect
from player import Player 
from game import Game
from card import Card

server = "25.29.74.26"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen() # needs to be tested with/without parameters
print("Waiting for connection")

all_cards = dict()

card_names = ["seven", "eight", "nine", "jack", "queen", "king", "ten", "ace"]
card_suits = ["clubs", "diamonds", "hearts", "spades"]
card_keys = []

for i in range(0, 32):
    card_name = card_names[i % 8]
    card_suit = card_suits[i // 8]
    key = card_name + "_" + card_suit
    card_keys.append(key)
    all_cards[key] = Card(card_name, card_suit, False, 0, 0)

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
                        winn = reply.eval_winner()
                        if winn != -1:
                            reply.update_score(winn)
                        reply.reset_moves()
                    elif data != "get":
                        reply.make_move(player, data)
                        reply.players_number_of_cards[player] -= 1

                    if idCount % 4 == 0:
                        reply.deal = True
                    else:
                        reply.deal = False
                    
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
