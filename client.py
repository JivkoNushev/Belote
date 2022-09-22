import pygame
import pickle
from network import Network
from player import Player
from card import Card
from game import Game

win_height = 1000
win_width = 1000

win = pygame.display.set_mode((win_height, win_width))
pygame.display.set_caption("Client")
pygame.init()
clientNumber = 0

def redrawWindow(win, game, player):
    win.fill((160,32,240))

    played_cards = game.moves
    players_number_of_cards = game.players_number_of_cards
    team_points = (game.t1_score, game.t2_score)
    first_player_id = player.get_id()
    player_id = player.get_id()
    player_start_x = (win_width - 8 * 50) // 2 # 50 is half of the width of a card
    player_start_y = win_height - 100 # 100 is the height of a card

    count = 0
    for i in range(0,players_number_of_cards[first_player_id]):
        player.cards[i].update_pos(player_start_x + count * 50, player_start_y)
        player.cards[i].draw(win)
        count += 1
    
    to_the_side = False
    for i in range(0,3):
        back_card = Card("back", "", False, 0, 0)
        player_id = (player_id + 1) % 4
        if i == 0:
            player_start_y = (win_height - 8 * 50) // 2
            player_start_x = win_width - 100
            back_card.update_body(pygame.transform.rotate(back_card.body_image, 90))
            to_the_side = True
        elif i == 1:
            player_start_x = (win_width - 8 * 50) // 2
            player_start_y = 0
            back_card.update_body(pygame.transform.rotate(back_card.body_image, 180))
            to_the_side = False
        else:
            player_start_y = (win_height - 8 * 50) // 2
            player_start_x = 0
            back_card.update_body(pygame.transform.rotate(back_card.body_image, 270))
            to_the_side = True

        count = 0
        for j in range(0, players_number_of_cards[player_id]):
            if to_the_side:
                back_card.update_pos(player_start_x, player_start_y + count * 50)
            else:
                back_card.update_pos(player_start_x + count * 50, player_start_y)
            back_card.draw(win)
            count += 1

    for i in range(0, 4):
        if played_cards[i] == 0:
            continue
        card = played_cards[i].split("_")
        back_card = Card(card[0], card[1], False, 0, 0)
        if i == first_player_id:
            player_start_x = win_width // 2 - 50 # 25 is one half of a card
            player_start_y = win_height / 2
        elif i == (first_player_id + 1) % 4:
            player_start_y = win_height // 2 - 25
            player_start_x = win_width // 2
            back_card.update_body(pygame.transform.rotate(back_card.body_image, 90))
        elif i == (first_player_id + 2) % 4:
            player_start_x = win_width // 2 - 50
            player_start_y = win_height // 2 - 100
            back_card.update_body(pygame.transform.rotate(back_card.body_image, 180))
        else:
            player_start_y = win_height // 2 - 25
            player_start_x = win_width // 2 - 100
            back_card.update_body(pygame.transform.rotate(back_card.body_image, 270))

        back_card.update_pos(player_start_x, player_start_y)
        back_card.draw(win)

    font = pygame.font.SysFont(None, 50)
    score1 = font.render(str(team_points[0]), True, (0, 0, 0))
    score2 = font.render(str(team_points[1]), True, (0, 0, 0))
    win.blit(score1, (0,0))
    win.blit(score2, (0,30))

    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player_id = int(n.getPlayer())
    player = Player(player_id, Game.deal_num_cards(8))

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.everyone_played():
            redrawWindow(win, game, player)
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
        #print(player_id)
        redrawWindow(win, game, player)

main()