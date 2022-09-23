import pygame
from card import Card
from player import Player
from game import Game

win_height = 1000
win_width = 1000

class Button:
    def __init__(self, x = 0, y = 0, width = 100, height = 50, color = (0,255,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def clicked(self, pos):
        return (self.x <= pos[0] and pos[0] < self.x + self.width) and (self.y <= pos[1] and pos[1] < self.y + self.height)

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
    playerID = font.render(str((player_id + 1) % 4), True, (0, 0, 0))
    win.blit(score1, (0,0))
    win.blit(score2, (0,30))
    win.blit(playerID, (win_width - 30,0))

    pygame.display.update()

def print_close_game(win):
    win.fill((160,32,240))
    wait_text = pygame.font.SysFont(None, 50).render("Game Ended/Somebody Left", True, (0, 0, 0))
    wait_text_rect = wait_text.get_rect(center=(win_width/2, win_height/2))
    win.blit(wait_text,wait_text_rect)
    pygame.display.update()

def print_wait_game(win):
    win.fill((160,32,240))
    wait_text = pygame.font.SysFont(None, 50).render("Waiting for players", True, (0, 0, 0))
    wait_text_rect = wait_text.get_rect(center=(win_width/2, win_height/2))
    win.blit(wait_text,wait_text_rect)
    pygame.display.update()

def print_main_menu(win):
    win.fill((0,200,50))
    wait_text = pygame.font.SysFont(None, 50).render("Main menu", True, (0, 0, 0))
    wait_text_rect = wait_text.get_rect(center=(win_width/2, win_height/2))
    win.blit(wait_text,wait_text_rect)
    for button in buttons:
        button.draw(win)
    pygame.display.update()

buttons = [Button(win_width/2, win_height/2 + 100)]