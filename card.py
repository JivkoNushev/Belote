import pygame

class Card:
    def __init__(self, name, suit, isTrump, x, y):
        self.x = x
        self.y = y
        self.name = name
        self.suit = suit
        self.isTrump = isTrump
        
        self.body_image = pygame.image.load("CardSprites/" + name + "_" + suit + ".png")
        self.body = self.body_image.get_rect()
        self.body.x = self.x
        self.body.y = self.y

        self.width = self.body_image.get_width()
        self.height = self.body_image.get_height()

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
        return (self.x <= pos[0] and pos[0] <= self.x + self.width - 50) and (self.y <= pos[1] and pos[1] <= self.y + self.height)
