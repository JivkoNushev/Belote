from cmath import rect
#from turtle import heading, width
import pygame

card_suits = ["clubs", "diamonds", "hearts", "spades"]
call_order = {"seven" : 0, "eight": 1, "nine" : 2, "ten": 3, "jack": 4, "queen": 5, "king": 6, "ace": 7}

class Player():
    def __init__(self, id, username):
        self.id = id
        self.cards = []
        self.username= username

    def get_id(self):
        return self.id

    def get_cards(self):
        return self.cards
    
    def call_belote(self, played_card):
        for card in self.get_cards():
            if card.get_name() != played_card.name and card.get_suit() == played_card.suit and (card.get_name() == "queen" or card.get_name() == "king"):
                print("belote!")
    
    def call_kare(self, sequences):
        list_t = [0, 0, 0, 0, 0, 0, 0, 0]
        for card in self.get_cards():
            list_t[call_order[card.get_name()]] += 1
        for i in range(2,8):
            if list_t[i] == 4:
                if i == 2:
                    print("150!")
                if i == 4:
                    print("200!")
                if i > 2 and i != 4:
                    print("100!")
                keys = call_order.keys()
                sequences.append("call_C_" + keys[i])
        return sequences
                
    def call_sequence(self):
        suit_cards = sequences = []
        sum_of_cards = 0
        for i in range(0,4):
            for card in self.get_cards():
                if card.get_suit() == card_suits[i]:
                    suit_cards.append(card) 
            if len(suit_cards) >= 5:
                for i in range(0, (len(suit_cards) - 4)):
                    for j in range(i, i + 5):
                        if int(call_order[suit_cards[i].get_name()] + j) != int(call_order[suit_cards[j].get_name()]):
                            break
                        else:
                            sum_of_cards += call_order[suit_cards[j].get_name()]
                            if j == i + 4:
                                if sum_of_cards % 5 == 0:
                                    sequences.append("call_K_" + call_order[suit_cards[i].get_name()])
                                    print("kvinta!")
                                else:
                                    sum_of_cards = 0
            
            if len(suit_cards) >= 4:
                for i in range(0, (len(suit_cards) - 3)):
                    for j in range(i, i + 4):
                        if int(call_order[suit_cards[i].get_name()] + j) != int(call_order[suit_cards[j].get_name()]):
                            break
                        else:
                            sum_of_cards += call_order[suit_cards[j].get_name()]
                            if j == i + 3:
                                if (sum_of_cards + 2) % 4 == 0:
                                    sequences.append("call_k_" + call_order[suit_cards[i].get_name()])
                                    print("kvadra!")
                                else:
                                    sum_of_cards = 0
                                    
            if len(suit_cards) >= 3:
                for i in range(0, (len(suit_cards) - 2)):
                    for j in range(i, i + 3):
                        if int(call_order[suit_cards[i].get_name()] + j) != int(call_order[suit_cards[j].get_name()]):
                            break
                        else:
                            sum_of_cards += call_order[suit_cards[j].get_name()]
                                
                            if j == i + 2:
                                if sum_of_cards % 3 == 0:
                                    sequences.append("call_T_" + call_order[suit_cards[i].get_name()])
                                    print("terca!")
                                else:
                                    sum_of_cards = 0 
           
            sum_of_cards = 0
            suit_cards = []
            
        self.call_kare(sequences)
    
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