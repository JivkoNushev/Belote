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
    item = ""
    items = []
    for s in str:
        if s == "(" or s == "," or s == ")":
            if item != "":
                items.append(int(item))
                item = ""
            continue
        item += s

    res = []
    while items:
        res.append((items[0], items[1]))
        items.pop(0)
        items.pop(0)

    return res

def make_pos(tup):
    res = ""
    count = 0
    for item in tup:
        if type(item) == int:
            if count % 2 == 0:
                res += "("
                res += str(item) + ","
            else:
                res += str(item) + "),"
        else:
            res += "("
            res += str(item[0]) + ","
            res += str(item[1]) + "),"
        count += 1
    return res[0:-1]

def player_data_todict(players):
    d = dict()
    count = 0
    for player in players:
        p = dict()
        p["color"] = player.get_color()
        p["pos"] = player.get_pos()
        p["width"] = player.get_width()
        p["height"] = player.get_height()
        d[count] = p
        count += 1 
    return d

def player_dict_tostr(playerDict):
    return str(playerDict)

def player_str_todict(playerDictString):
    res = dict()
    playerDictString = playerDictString[1:-1]
    count = 0
    while playerDictString:
        res2 = dict()
        if playerDictString[0] == "}":
            break
        while playerDictString[0] != "{":
            playerDictString = playerDictString[1:]
        playerDictString = playerDictString[1:]
        
        for i in range(4):
            key = ""
            while playerDictString[0] != "'":
                playerDictString = playerDictString[1:]
            playerDictString = playerDictString[1:]
            
            while playerDictString[0] != "'":
                key += playerDictString[0]
                playerDictString = playerDictString[1:]
            playerDictString = playerDictString[1:]
            
            while(playerDictString[0] == ":" or playerDictString[0] == " " or playerDictString[0] == "," or playerDictString[0] == "}"):
                playerDictString = playerDictString[1:]
                
            item = ""
            if playerDictString[0] == "(":
                playerDictString = playerDictString[1:]
                while playerDictString[0] != ")":
                    item += playerDictString[0]
                    playerDictString = playerDictString[1:]
                playerDictString = playerDictString[1:]
            else:
                while playerDictString[0] != "," and playerDictString[0] != "}":
                    item += playerDictString[0]
                    playerDictString = playerDictString[1:]
            playerDictString = playerDictString[1:]
            res2[key] = eval(item)
        res[count] = res2.copy()
        count += 1
    return res

pos = [(0, 0), (100, 100), (200, 200), (300, 300)]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            PlayerData = player_str_todict(conn.recv(2048).decode("utf-8"))
            
            pos[player] = PlayerData[player]["pos"]
            if not PlayerData:
                print("Disconnected")
                break
            # else:
            #     if player == 0:
            #         reply = (pos[1], pos[2], pos[3])
            #     elif player == 1:
            #         reply = (pos[0], pos[2], pos[3])
            #     elif player == 2:
            #         reply = (pos[0], pos[1], pos[3])
            #     else:
            #         reply = (pos[0], pos[1], pos[2])
               
            #    print("Received: ", data[0])
            #    print("Sending: ", reply)

            conn.sendall(str.encode(player_dict_tostr(PlayerData)))
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
