from cmath import rect
from turtle import heading, width
import pygame

class Player():
    def __init__(self, id, cards):
        self.id = id
        if type(cards) != list:
            self.cards = [cards]
        elif cards == 0:
            cards = []
        else:
            self.cards = cards

    def get_id(self):
        return self.id

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

    def get_card(self,card):
        self.cards.append(card)

    def play_turn(self, card_number, cards_on_table):
        cards_on_table.append(self.cards[card_number])
        del self.cards[card_number]
