import pygame
from network import Network

win_height = 500
win_width = 500

win = pygame.display.set_mode((win_height, win_width))
pygame.display.set_caption("Client")

clientNumber = 0

class Player():
    def __init__(self, x, y, width , height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.velocity = 3

    def get_color(self):
        return self.color

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_pos(self):
        return (self.x, self.y)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.y += self.velocity

        if keys[pygame.K_UP]:
            self.y -= self.velocity

        if keys[pygame.K_RIGHT]:
            self.x += self.velocity

        if keys[pygame.K_LEFT]:
            self.x -= self.velocity

        po = pygame.mouse.get_pressed()
        if po[0]:
            mPos = pygame.mouse.get_pos()
            if (self.x <= mPos[0] and mPos[0] <= self.x + self.width) and (self.y <= mPos[1] and mPos[1] <= self.y + self.height):
                self.color = (0,0,255)
            else:
                self.color = (0,255,0)


        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

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

def redrawWindow(win, players):
    win.fill((255,255,255))
    for player in players:
        player.draw(win)

    pygame.display.update()

def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    players = [Player(startPos[0][0], startPos[0][1],100,100,(0,255,0)), Player(0,0,100,100,(255,0,0)), Player(0,0,100,100,(255,0,0)), Player(0,0,100,100,(255,0,0))]
    
    p = players[0]

    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        playersDict = player_data_todict(players)
        #print(player_dict_tostr(playersDict))

        pDict = player_str_todict(n.send(player_dict_tostr(playersDict)))
        #print(pDict)
        count = 0
        for player in players:
            if count == 0:
                count += 1
                continue
            player.x = pDict[count]["pos"][0]
            player.y = pDict[count]["pos"][1]
            player.color = pDict[count]["color"]
            player.update()
            count += 1
        #print(p.get_pos())
        #print(players[0].get_pos())
        #print(players[0].color)
        #print("\t\t\t\t\t\t" + str(players[1].get_pos()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        players[0].move()
        redrawWindow(win, players)

main()