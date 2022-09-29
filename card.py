import pygame
from settings import _settings

pygame.display.init()
#win_width, win_height = pygame.display.get_surface().get_size()

_settings.change_win_width_height(pygame.display.Info().current_w, pygame.display.Info().current_h)

win_height = _settings.win_width / 2
win_width = _settings.win_height / 2

#win_height = 1280
#win_width = 720

class Card:
    def __init__(self, x, y, name, suit, width = 1, height = 1, isTrump = False):
        self.name = name
        self.suit = suit
        
        if width <= 0:
            width = 1
        if height <= 0:
            height = 1

        self.width = win_width // 100 + width * win_width // 100
        self.height = win_height // 100 + height * win_height // 100
        
        self.x = win_width//2 + x * win_width // 100
        self.y = win_height//2 + y * win_height // 100
        
        self.isTrump = isTrump
        
        self.body_image = pygame.transform.scale(pygame.image.load("CardSprites/" + name + "_" + suit + ".png"), (self.width, self.height))
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_name(self):
        return self.name
    
    def get_suit(self):
        return self.suit

    def update_pos(self, x, y):
        self.x = x
        self.y = y
        self.body.x = x
        self.body.y = y

    def update_body(self, new_body_image):
        self.body = new_body_image.get_rect()
        self.body_image = new_body_image

    def draw(self, win):
        win.blit(self.body_image, self.body)
    
    def clicked(self, pos):
        return (self.x <= pos[0] and pos[0] <= self.x + self.width / 2) and (self.y <= pos[1] and pos[1] <= self.y + self.height)
