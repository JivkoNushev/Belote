from operator import truediv
import pygame
import ui as ui
from network import Network
from player import Player
from settings import _settings
#from card import Card
#from game import Game
pygame.init()

pygame.display.init()

_settings.change_win_width_height(pygame.display.Info().current_w, pygame.display.Info().current_h)

win_height = _settings.win_width / 2
win_width = _settings.win_height / 2

#win_height = 1280
#win_width = 720

win = pygame.display.set_mode((win_height, win_width), pygame.RESIZABLE)
surface = pygame.display.get_surface()
pygame.display.set_caption("Client")

clientNumber = 0

def main():
    clock = pygame.time.Clock()
    run = True
    main_menu_loop = False

    while main_menu_loop:
        ui.print_main_menu(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ui.buttons["main_menu"].clicked(pos):
                    main_menu_loop = False

    n = Network()
    player_id = int(n.getPlayer())
    player = Player(player_id)
    dealt_third = False

    while run:
        win_width, win_height = pygame.display.get_surface().get_size()
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            ui.print_close_game(win)
            pygame.time.delay(2000)
            print("Couldn't get game")
            break

        dealt_first = False
        dealt_second = False
        
        while not game.playing:
            win_width, win_height = pygame.display.get_surface().get_size()
            dealt_third = False

            game = n.send("get")
            if game.deal == True and game.deal_turn == player_id and dealt_first == False:
                player.deal(game.deal_num_cards(3))
                game = n.send("deal3")
                dealt_first = True
            elif game.deal == True and game.deal_turn == player_id and dealt_first == True and dealt_second == False:
                player.deal(game.deal_num_cards(2))
                game = n.send("deal2")
                dealt_second = True
            if not dealt_first or not dealt_second or game.players_number_of_cards.count(5) != 4:
                ui.print_wait_game(win)
                game = n.send("get")
                continue
            #print(game.players_number_of_cards)
            ui.redrawWindow(win, game, player, True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if game.change_type_turn == player_id:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        game_type = ""
                        if ui.buttons["pass"].clicked(pos):
                            game_type = "pass"
                        elif ui.buttons["clubs"].clicked(pos):
                            game_type = "clubs"
                        elif ui.buttons["diamonds"].clicked(pos):
                            game_type = "diamonds"
                        elif ui.buttons["hearts"].clicked(pos):
                            game_type = "hearts"
                        elif ui.buttons["spades"].clicked(pos):
                            game_type = "spades"
                        elif ui.buttons["no_trumps"].clicked(pos):
                            game_type = "no_trumps"
                        elif ui.buttons["all_trumps"].clicked(pos):
                            game_type = "all_trumps"
                        elif ui.buttons["2x"].clicked(pos):
                            game_type = "2x"
                        elif ui.buttons["4x"].clicked(pos):
                            game_type = "4x"

                        if game.can_call_game_type(game_type, player_id):
                            print(game_type)
                            game = n.send(game_type)
                        print(game.types_calls)
                        

        while dealt_third == False:
            win_width, win_height = pygame.display.get_surface().get_size()
            if game.deal == True and game.deal_turn == player_id and dealt_second == True and dealt_third == False:
                player.deal(game.deal_num_cards(3))
                game = n.send("deal3")
                player.cards = game.order_cards(player.cards)
                dealt_third = True
                break
            game = n.send("get")
            ui.print_wait_game(win)

        if game.everyone_played():
            ui.redrawWindow(win, game, player)
            pygame.time.delay(1000)
            try:
                game = n.send("reset")
                continue
            except:
                run = False
                print("Couldn't get game")
                break

        if game.ended() and game.type != "":
            try:
                game = n.send("get_type")
                
                dealt_third = False
                continue
            except:
                run = False
                print("failed")
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
                                game.call(player, card)
                                player.get_cards().remove(card)
                                game = n.send(move)
        ui.redrawWindow(win, game, player)

main()