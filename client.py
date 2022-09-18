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
all_cards = {"nine_clubs" : Card("nine", "clubs", False, 100,100), "nine_spades" : Card("nine", "spades", False, 300,100)}
def redrawWindow(win, cards):
    win.fill((255,255,255))
    for card in cards:
        if card == 0:
            break
        all_cards[card].draw(win)
    pygame.display.update()

cards = ["nine_clubs"]
cards2 = ["nine_spades"]

def main():
    run = True
    clock = pygame.time.Clock()

    n = Network()
    player = int(n.getPlayer())
    p1 = Player([all_cards[cards[0]], all_cards[cards2[0]]])
    p2 = Player(all_cards[cards2[0]])
    players = [p1,p2]
    redrawWindow(win, cards)
    redrawWindow(win, cards2)
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
                if game.turn == player:
                    for card in players[player].cards:
                        if card.clicked(pos):
                            move = card.name + "_" + card.suit
                            game = n.send(move)
        count = 0
        for card in game.get_moves():
            if card != 0:
                all_cards[card].update_card(50 + count * 50, 200)
                count += 1

        redrawWindow(win, game.get_moves())

main()