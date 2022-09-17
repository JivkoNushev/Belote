import pygame
import pickle
from network import Network
from player import Player
from player import Card

win_height = 500
win_width = 500

win = pygame.display.set_mode((win_height, win_width))
pygame.display.set_caption("Client")

clientNumber = 0

def redrawWindow(win, player):
    win.fill((255,255,255))
    player.draw(win)
    pygame.display.update()

cards = [Card("nine", "clubs", False, 100,100), Card("nine", "spades", False, 300,100)]

def main():
    run = True
    clock = pygame.time.Clock()

    n = Network()
    player = int(n.getPlayer())
    players = [Player(cards), 0, 0, 0]

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
        
        if game.both_played():
            redrawWindow()
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for card in cards:
                    print(pos)
                    print(card.x)
                    print(card.y)
                    if card.clicked(pos):
                        players[0].cards[0].update_card(50,0)

        redrawWindow(win, players[player])

main()