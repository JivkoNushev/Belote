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

    def has_suit(self, suit):
        for card in self.get_cards():
            if card.get_suit() == suit:
                return True
                
        return False

    def draw(self, win):
        for card in self.cards:
            card.draw(win)
