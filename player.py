from cmath import rect
from turtle import heading, width
import pygame

class Player():
    def __init__(self, id):
        self.id = id
        self.cards = []

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

    def deal(self, cards):
        for card in cards:
            self.cards.append(card)

