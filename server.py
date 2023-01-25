import socket
import pickle
from _thread import *
from game import Game
from card import Card

server = "192.168.1.184"
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
    all_cards[key] = Card(0,0,card_name, card_suit, False)

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

                    elif len(data) > 9 and data[0:9] == "username_":
                        reply.usernames[player] = data[9:]

                    elif data == "deal3":
                        for i in range(0,3):
                            reply.deck.pop(0)
                        reply.deal_turn = (reply.deal_turn + 1) % 4
                        reply.players_number_of_cards[player] += 3
                    
                    elif data == "deal2":
                        for i in range(0,2):
                            reply.deck.pop(0)
                        reply.deal_turn = (reply.deal_turn + 1) % 4
                        reply.players_number_of_cards[player] += 2

                    elif data == "get_type":
                        reply.update_points()
                        reply.type = ""
                        reply.change_type_turn == reply.turn
                        reply.reset_deck()
                        reply.playing = False
                        reply.players_number_of_cards = [0,0,0,0]
                        reply.types_calls = [0,0,0,0]
                        reply.called_by_team = 0
                        reply.t1_score = 0
                        reply.t2_score = 0
                        reply.reset_moves()
                        reply.made_calls = False
                        reply.player_calls = {0: [],1: [],2: [],3: []}
                        reply.belote = [0,0,0,0]


                    elif len(data) > 4 and data[0:5] == "call_":
                        reply.player_calls[player].append(data[5:])
                        #print(reply.player_calls[player])

                    elif data == "change_calls":
                        if reply.made_calls == False:
                            reply.change_calls()

                    elif data == "belote":
                        if player % 2 == 0:
                            reply.t1_score += 20
                        else:
                            reply.t2_score += 20
                        reply.Belote[player] = True

                    elif data == "clear_belote":
                        reply.Belote[player] = False

                    elif data == "pass": 
                        if reply.types_calls.count("pass") == 3:
                            reply.type = ""
                            reply.trump = ""
                            reply.score_multiplier = 1
                            reply.types_calls = [0,0,0,0]
                            reply.turn = (reply.turn + 1)%4
                            reply.change_type_turn = reply.turn

                        elif reply.types_calls.count(0) > 1:
                            reply.types_calls[player] = data
                            reply.change_type_turn = (reply.change_type_turn + 1)%4

                        else:
                            reply.types_calls[player] = data
                            reply.playing = True

                    elif data == "clubs" or data == "diamonds" or data == "hearts" or data == "spades":
                        reply.type = "suit_trump"
                        reply.trump = data
                        reply.score_multiplier = 1
                        reply.types_calls = [0,0,0,0]
                        reply.types_calls[player] = data
                        reply.change_type_turn = (reply.change_type_turn + 1)%4
                        reply.called_by_team = player % 2

                    elif data == "no_trumps":
                        reply.type = "no_trumps"
                        reply.trump = 0
                        reply.score_multiplier = 1
                        reply.types_calls = [0,0,0,0]
                        reply.types_calls[player] = data
                        reply.change_type_turn = (reply.change_type_turn + 1)%4
                        reply.called_by_team = player % 2

                    elif data == "all_trumps":
                        reply.type = "all_trumps"
                        reply.trump = 0
                        reply.score_multiplier = 1
                        reply.types_calls = [0,0,0,0]
                        reply.types_calls[player] = data
                        reply.change_type_turn = (reply.change_type_turn + 1)%4
                        reply.called_by_team = player % 2

                    elif data == "2x":
                        reply.score_multiplier = 2
                        reply.types_calls[player] = data
                        reply.change_type_turn = (reply.change_type_turn + 1)%4
                        reply.called_by_team = player % 2

                    elif data == "4x":
                        reply.score_multiplier = 4
                        reply.types_calls[player] = data
                        reply.change_type_turn = (reply.change_type_turn + 1)%4
                        reply.called_by_team = player % 2

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