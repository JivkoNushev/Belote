from turtle import heading, width
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

    def update_card(self, x, y):
        self.body.x = x
        self.body.y = y

    def draw(self, win):
        win.blit(self.body_image, self.body)
    
    def clicked(self, pos):
        return (self.x <= pos[0] and pos[0] <= self.x + self.width) and (self.y <= pos[1] and pos[1] <= self.y + self.height)

all_cards = {"nine_clubs" : Card("nine", "clubs", False, 100,100), "nine_spades" : Card("nine", "spades", False, 300,100)}

class Player():
    def __init__(self, cards):
        if type(cards) != list:
            self.cards = [cards]
        else:
            self.cards = cards

    def get_cards(self):
        return self.cards

    def draw(self, win):
        for card in self.cards:
            card.draw(win)

    def move(self):
        po = pygame.mouse.get_pressed()
        if po[0]:
            mPos = pygame.mouse.get_pos()
            if (self.x <= mPos[0] and mPos[0] <= self.x + self.width) and (self.y <= mPos[1] and mPos[1] <= self.y + self.height):
                self.color = (0,0,255)
            else:
                self.color = (0,255,0)

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)