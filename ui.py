import pygame
from card import Card
from player import Player
from game import Game
from settings import _settings

pygame.display.init()

_settings.change_win_width_height(pygame.display.Info().current_w, pygame.display.Info().current_h)

win_height = _settings.win_height / 2
win_width = _settings.win_width / 2

#win_height = 720
#win_width = 1280

class Button:
    def __init__(self, text, x, y, width = 1, height = 1, color = (0,255,0)):
        if width <= 0:
            width = 1
        if height <= 0:
            height = 1

        self.width_multiplier = width
        self.height_multiplier = height
        self.x_multiplier = x
        self.y_multiplier = y

        self.width = win_width // 100 + width * win_width // 100
        self.height = win_height // 100 + height * win_height // 100
        
        self.x = win_width//2 + x * win_width // 100
        self.y = win_height//2 + y * win_height // 100
        
        self.color = color
        self.text = text

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def update(self, win_width, win_height):
        self.width = win_width // 100 + self.width_multiplier * win_width // 100
        self.height = win_height // 100 + self.height_multiplier * win_height // 100
        
        self.x = win_width//2 + self.x_multiplier * win_width // 100
        self.y = win_height//2 + self.y_multiplier * win_height // 100
    def clicked(self, pos):
        if (self.x <= pos[0] and pos[0] < self.x + self.width) and (self.y <= pos[1] and pos[1] < self.y + self.height):
            #self.color = (0,0,255)
            return True
        return False

buttons = {"enter_game": Button("Enter Game", 0, 0,20, 10), "clubs": Button("Clubs", -30, -30, 20, 10), "diamonds": Button("Diamonds", -30, -20, 20, 10), "hearts": Button("Hearts", -30, -10, 20, 10), "spades":Button("Spades", -30, 0, 20, 10), "no_trumps": Button("no_trumps", 10, -30, 20, 10),\
"all_trumps":Button("all_trumps", 10, -20, 20, 10), "2x":Button("2x", 10, -10, 20, 10), "4x":Button("4x", 10, 0, 20, 10), "pass":Button("Pass", -30, 20, 20 * 3, 10)}

def redrawWindow(win, game, player, choosing_game_type = False):
    win_width, win_height = pygame.display.get_surface().get_size()
    win.fill((100,255,100))
    # print(game.type)
    
    if choosing_game_type == True:
        for key, button in buttons.items():
            button.update(win_width, win_height)
            if key == "enter_game":
                continue

            if game.type == key or game.trump == key:
                button.color = (144,238,144)
            elif key == "2x":
                if game.score_multiplier == 2:
                    button.color = (144,238,144)
                else:
                    button.color = (0,255, 0)
            elif key == "4x":
                if game.score_multiplier == 4:
                    button.color = (144,238,144)
                else:
                    button.color = (0,255, 0)
            elif key == "pass":
                button.color = (0,255, 0)
            elif game.type == "suit_trump" and game.gameTypes[key] > game.gameTypes[game.trump]:
                button.color = (0,255, 0)
            elif game.type == "" or game.gameTypes[key] > game.gameTypes[game.type]:
                button.color = (0,255, 0)
            else:
                button.color = 	(0,100,0)
                
            button.draw(win)
            wait_text = pygame.font.SysFont(None, int( win_height / 20)).render(button.text, True, (0, 0, 0))
            wait_text_rect = wait_text.get_rect(center=(button.x, button.y))
            wait_text_rect.width = button.width
            wait_text_rect.height = button.height
            wait_text_rect.x = wait_text_rect.x + wait_text_rect.width / 2
            wait_text_rect.y = wait_text_rect.y + wait_text_rect.height / 2
            win.blit(wait_text, wait_text_rect)

    # table_image = pygame.image.load("CardSprites/table_.png")
    # table_image = pygame.transform.scale(table_image, (win_width, win_height))
    # table_body = table_image.get_rect()
    # win.blit(table_image, table_body)

    played_cards = game.moves
    players_number_of_cards = game.players_number_of_cards
    team_points = (game.t1_points, game.t2_points)
    first_player_id = player.get_id()
    player_id = player.get_id()
    card_temp = Card(0,0, "back", "", 15,10)
    player_start_x = (win_width - (card_temp.width / 2 * (players_number_of_cards[player_id] + 1))) // 2
    player_start_y = win_height - card_temp.height 

    count = 0
    #for i in range(0, players_number_of_cards[player_id]):
    for card in player.cards:
        card.update_pos(player_start_x + count * card_temp.width / 2, player_start_y)
        card.draw(win)
        count += 1

    f_coords = (player_start_x, player_start_y-( win_height / 20))
    username_color = (0,0,0)
    if game.playing:
        if game.turn == player_id:
            username_color = (255,0,0)
    elif game.change_type_turn == player_id:
        username_color = (255,0,0)
    username_text = pygame.font.SysFont(None, int( win_height / 20)).render(game.usernames[first_player_id], True, username_color)
    win.blit(username_text, f_coords)

    count += 1
    if game.types_calls[first_player_id] and game.playing == False:
        wait_text = pygame.font.SysFont(None, int( win_height / 20)).render(game.types_calls[first_player_id], True, (0, 0, 0))
        wait_text_rect = pygame.Rect(player_start_x + count * card_temp.width / 2, player_start_y, card_temp.width, card_temp.height)
        win.blit(wait_text,wait_text_rect)

    to_the_side = False
    for i in range(0, 3):
        back_card = Card(0,0,"back", "", 15, 10)
        player_id = (player_id + 1) % 4
        coords = (0,0)
        username_color = (0,0,0)
        if game.playing:
            if game.turn == player_id:
                username_color = (255,0,0)
        elif game.change_type_turn == player_id:
            username_color = (255,0,0)
        username = pygame.font.SysFont(None, int( win_height / 20)).render(game.usernames[player_id], True, username_color) 
        if i == 0:
            player_start_y = (win_height - (back_card.width / 2 * (players_number_of_cards[player_id] + 1))) // 2
            player_start_x = win_width - back_card.height
            back_card.update_body(pygame.transform.rotate(back_card.body_image, 90))
            username = pygame.transform.rotate(username, 90)
            coords = (player_start_x - ( win_height / 20), player_start_y)
            to_the_side = True
        elif i == 1:
            player_start_x = (win_width - (back_card.width / 2 * (players_number_of_cards[player_id] + 1))) // 2
            player_start_y = 0
            back_card.update_body(pygame.transform.rotate(back_card.body_image, 180))
            username = pygame.transform.rotate(username, 180)
            coords = (player_start_x, back_card.height)
            to_the_side = False
        else:
            player_start_y = (win_height - (back_card.width / 2 * (players_number_of_cards[player_id] + 1))) // 2
            player_start_x = 0
            back_card.update_body(pygame.transform.rotate(back_card.body_image, 270))
            username = pygame.transform.rotate(username, 270)
            coords = (player_start_x + back_card.height, player_start_y)
            to_the_side = True
        win.blit(username, coords)
        type_call = game.types_calls[player_id]
        if type_call != 0 and game.playing == False:
            if i == 0:
                call_y = (win_height - (back_card.width / 2 * (players_number_of_cards[player_id] + 1))) // 2
                call_x = win_width - back_card.height 
                call_y += (back_card.width / 2 * (players_number_of_cards[player_id] + 1))
                call_text = pygame.font.SysFont(None, int( win_height / 20)).render(type_call, True, (0, 0, 0))
                call_text_rect = pygame.Rect(call_x, call_y, back_card.width, back_card.height)
                win.blit(call_text,call_text_rect)
            elif i == 1:
                call_x = (win_width - (back_card.width / 2 * (players_number_of_cards[player_id] + 1))) // 2
                call_y = 0
                call_x += (back_card.width / 2 * (players_number_of_cards[player_id] + 1))
                call_text = pygame.font.SysFont(None, int( win_height / 20)).render(type_call, True, (0, 0, 0))
                call_text_rect = pygame.Rect(call_x, call_y, back_card.width, back_card.height)
                win.blit(call_text,call_text_rect)
            else:
                call_y = (win_height - (back_card.width / 2 * (players_number_of_cards[player_id] + 1))) // 2
                call_x = 0
                call_y += (back_card.width / 2 * (players_number_of_cards[player_id] + 1))
                call_text = pygame.font.SysFont(None, int( win_height / 20)).render(type_call, True, (0, 0, 0))
                call_text_rect = pygame.Rect(call_x, call_y, back_card.width, back_card.height)
                win.blit(call_text,call_text_rect)

        
        count = 0
        for j in range(0, players_number_of_cards[player_id]):
            if to_the_side:
                back_card.update_pos(player_start_x, player_start_y + count * back_card.width / 2)
            else:
                back_card.update_pos(player_start_x + count * back_card.width / 2, player_start_y)
            back_card.draw(win)
            count += 1

    for i in range(0, 4):
        if played_cards[i] == 0:
            continue
        card = played_cards[i].split("_")
        back_card = Card(0,0,card[0], card[1], 15, 10, False)
        if i == first_player_id:
            player_start_x = win_width // 2 - back_card.width
            player_start_y = win_height / 2
        elif i == (first_player_id + 1) % 4:
            player_start_y = win_height // 2 - back_card.width / 2
            player_start_x = win_width // 2
            back_card.update_body(pygame.transform.rotate(back_card.body_image, 90))
        elif i == (first_player_id + 2) % 4:
            player_start_x = win_width // 2 - back_card.width
            player_start_y = win_height // 2 - back_card.height
            back_card.update_body(pygame.transform.rotate(back_card.body_image, 180))
        else:
            player_start_y = win_height // 2 - back_card.width/2
            player_start_x = win_width // 2 - back_card.height
            back_card.update_body(pygame.transform.rotate(back_card.body_image, 270))

        

        back_card.update_pos(player_start_x, player_start_y)
        back_card.draw(win)

    font = pygame.font.SysFont(None, int( win_height / 20))
    score1 = font.render(str(team_points[0]), True, (0, 0, 0))
    score2 = font.render(str(team_points[1]), True, (0, 0, 0))
    playerID = font.render(str((player_id + 1) % 4), True, (0, 0, 0))
    gameType = font.render(game.type, True, (0, 0, 0))
    
    win.blit(score1, (0,0))
    win.blit(score2, (0,30))
    win.blit(playerID, (win_width - 30,0))
    win.blit(gameType, (0,60))

    pygame.display.update()

def print_close_game(win):
    win.fill((160,32,240))
    wait_text = pygame.font.SysFont(None, int( win_height / 20)).render("Game Ended/Somebody Left", True, (0, 0, 0))
    wait_text_rect = wait_text.get_rect(center=(win_width/2, win_height/2))
    win.blit(wait_text,wait_text_rect)
    pygame.display.update()

def print_wait_game(win):
    win.fill((160,32,240))
    wait_text = pygame.font.SysFont(None, int( win_height / 20)).render("Waiting for players", True, (0, 0, 0))
    wait_text_rect = wait_text.get_rect(center=(win_width/2, win_height/2))
    win.blit(wait_text,wait_text_rect)
    pygame.display.update()

input_rect = pygame.Rect(200, 200, 140, 32)

def print_main_menu(win, active, username):
    win.fill((0,200,50))
    wait_text = pygame.font.SysFont(None, int( win_height / 20)).render("Main menu", True, (0, 0, 0))
    wait_text_rect = wait_text.get_rect(center=(win_width/2, win_height/2))
    win.blit(wait_text,wait_text_rect)
    
    buttons["enter_game"].draw(win)
    enter_game_text = pygame.font.SysFont(None, int( win_height / 20)).render("Enter Game", True, (0, 0, 0))
    enter_game_rect = enter_game_text.get_rect(center=(buttons["enter_game"].x, buttons["enter_game"].y))
    enter_game_rect.width = buttons["enter_game"].width
    enter_game_rect.height = buttons["enter_game"].height
    enter_game_rect.x = enter_game_rect.x + enter_game_rect.width / 2
    enter_game_rect.y = enter_game_rect.y + enter_game_rect.height / 2
    win.blit(enter_game_text, enter_game_rect)

    base_font = pygame.font.SysFont(None, int( win_height / 20))
    
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    if active:
        color = color_active
    else:
        color = color_passive
    pygame.draw.rect(win, color, input_rect)
    text_surface = base_font.render(username, True, (255, 255, 255))
    win.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    input_rect.w = max(100, text_surface.get_width()+10)

    pygame.display.update()


