from cmath import rect
from turtle import heading, width
import pygame

card_suits = ["clubs", "diamonds", "hearts", "spades"]
call_order = {"seven" : 0, "eight": 1, "nine" : 2, "ten": 3, "jack": 4, "queen": 5, "king": 6, "ace": 7}

class Player():
    def __init__(self, id):
        self.id = id
        self.cards = []

    def get_id(self):
        return self.id

    def get_cards(self):
        return self.cards
    
    def call(self):
        suit_cards = []
        sum_of_cards = 0
        for i in range(0,4):
            number = 0
            for card in self.get_cards():
                if card.get_suit() == card_suits[i]:
                    sum_of_cards += call_order[card.get_name()]
                    suit_cards.append(card)
            if len(suit_cards) == 5 and sum_of_cards % 5 == 0:
                number = 5
            elif len(suit_cards) == 4 and (sum_of_cards + 2) % 4 == 0:
                number = 4
            elif len(suit_cards) == 3 and sum_of_cards % 3 == 0:
                number = 3
            
            for i in range(0, number):
                if i == number - 1:
                    if number == 5:
                        print("kvinta!")
                    if number == 4:
                        print("kvadra!")
                    if number == 3:
                        print("terca!")
                else:
                    print("i = ", i, "number = ", number, "len = ", len(suit_cards))
                    if int(call_order[suit_cards[0].get_name()]+i) != int(call_order[suit_cards[i].get_name()]):
                        break
            
            sum_of_cards = 0
            suit_cards = []
    
    def has_suit(self, suit):
        for card in self.get_cards():
            if card.get_suit() == suit:
                return True
                
        return False

    def has_higher(self, move, TrumpsOrder):
        pcard_name = move[0]
        pcard_suit = move[1]
    
        for card in self.get_cards():
            if card.get_suit() == pcard_suit and TrumpsOrder[card.get_name()] > TrumpsOrder[pcard_name]:
                return True
            
        return False
    
    def draw(self, win):
        for card in self.cards:
            card.draw(win)
    
    def deal(self, cards):
        for card in cards:
            self.cards.append(card)