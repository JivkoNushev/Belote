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

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def redrawWindow(win, players):
    win.fill((255,255,255))
    for player in players:
        player.draw(win)

    pygame.display.update()

def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    players = [Player(startPos[0], startPos[1],100,100,(0,255,0)), Player(0,0,100,100,(0,255,0)), Player(0,0,100,100,(0,255,0)), Player(0,0,100,100,(0,255,0))]
    p = players[0]

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        pPos = read_pos(n.send(make_pos((p.x, p.y))))
        count = 0

        for player in players:
            if count > 0:
                player.x = pPos[count][0]
                player.y = pPos[count][1]
                player.update()
            count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, players)

main()