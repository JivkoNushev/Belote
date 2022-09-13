import pygame
import pickle
from network import Network
from player import Player

win_height = 500
win_width = 500

win = pygame.display.set_mode((win_height, win_width))
pygame.display.set_caption("Client")

clientNumber = 0

def redrawWindow(win, players):
    win.fill((255,255,255))
    for player in players:
        player.draw(win)

    pygame.display.update()

def main():
    run = True
    n = Network()
    p1 = n.getPlayer()
    players = [p1, 0, 0, 0]
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        otherPlayers = n.send(p1)
        for i in range(1,4):
            players[i] = otherPlayers[i-1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        players[0].move()
        redrawWindow(win, players)

main()