from operator import truediv
import pygame
import pickle
import ui as ui
from network import Network
from player import Player
from card import Card
from game import Game

win = pygame.display.set_mode((ui.win_height, ui.win_width))
pygame.display.set_caption("Client")
pygame.init()
clientNumber = 0

def main():
    run = True
    clock = pygame.time.Clock()
    main_menu = True
    while main_menu:
        ui.print_main_menu(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in ui.buttons:
                    if button.clicked(pos):
                        main_menu = False

    n = Network()
    player_id = int(n.getPlayer())
    dealt = False

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            ui.print_close_game(win)
            pygame.time.delay(2000)
            print("Couldn't get game")
            break
        if game.deal == True and dealt == False and game.deal_turn == player_id:
            player = Player(player_id, game.deal_num_cards(8))
            game = n.send("deal8")
            dealt = True
        if not dealt:
            ui.print_wait_game(win)
            continue

        if game.everyone_played():
            ui.redrawWindow(win, game, player)
            pygame.time.delay(1000)
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
                ui.print_close_game()
                pygame.time.delay(2000)
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if game.turn == player_id:
                    for card in player.cards:
                        if card.clicked(pos):
                            move = card.name + "_" + card.suit
                            if game.check_move(move, player) == True:
                                player.get_cards().remove(card)
                                game = n.send(move)
        ui.redrawWindow(win, game, player)

main()