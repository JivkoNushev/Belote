import enum
import random
from card import Card
from player import Player

all_cards = dict()

card_names = ["seven", "eight", "nine", "jack", "queen", "king", "ten", "ace"]
card_suits = ["clubs", "diamonds", "hearts", "spades"]
card_keys = []

for i in range(0, 32):
    card_name = card_names[i % 8]
    card_suit = card_suits[i // 8]
    key = card_name + "_" + card_suit
    card_keys.append(key)
    all_cards[key] = Card(card_name, card_suit, False, 0, 0)

class Game:
    def __init__(self, id):
        self.id = id
        self.t1_score = 0
        self.t2_score = 0
        self.moves = [0,0,0,0]
        self.players_number_of_cards = [8,8,8,8]
        self.turn = 0
        self.deal_turn = 0
        self.type = "no_trumps"
        self.trump = ""
        self.deal = False
        self.deck = card_keys
        random.shuffle(self.deck)
        self.noTrumpsOrder = {"seven" : 0, "eight": 1, "nine" : 2, "jack": 3, "queen": 4, "king": 5, "ten": 6, "ace": 7}
        self.TrumpsOrder = {"seven" : 0, "eight": 1, "queen": 2, "king": 3, "ten": 4, "ace": 5, "nine" : 6, "jack": 7}

        self.noTrumpsValue = {"seven" : 0, "eight": 0, "nine" : 0, "jack": 2, "queen": 3, "king": 4, "ten": 10, "ace": 11}
        self.TrumpsValue = {"seven" : 0, "eight": 0, "queen": 3, "king": 4, "ten": 10, "ace": 11, "nine" : 14, "jack": 20}
        
    def get_moves(self):
        return self.moves

    def get_player_move(self, player):
        pass

    def make_move(self, player, move):
        self.moves[player] = move
        self.turn = (self.turn + 1) % 4

    def connected(self):
        pass

    def everyone_played(self):
        for move in self.moves:
            if move == 0:
                return False
        return True

    def all_trumps(self):
        best_card = self.moves[self.turn].split("_")
        winn = self.turn

        for i in range(0,4):
            if self.moves[i] != 0:
                card = self.moves[i].split("_")
                if card[1] == best_card[1]:
                    if self.TrumpsOrder[card[0]] > self.TrumpsOrder[best_card[0]]:
                        best_card[0] = card[0]
                        winn = i
        
        return winn

    def no_trumps(self):
        best_card = self.moves[self.turn].split("_")
        winn = self.turn

        for i in range(0,4):
            if self.moves[i] != 0:
                card = self.moves[i].split("_")
                if card[1] == best_card[1]:
                    if self.noTrumpsOrder[card[0]] > self.noTrumpsOrder[best_card[0]]:
                        best_card[0] = card[0]
                        winn = i
        
        return winn

    def suit_trump(self, suit):
        best_card = self.moves[self.turn].split("_")
        winn = self.turn
        trumps_in_game = 0
        
        for i in range(0,4):
            if self.moves[i] != 0:
                card = self.moves[i].split("_")
                if card.isTrump:
                    trumps_in_game += 1
                
                if trumps_in_game == 0:
                    if card[1] == best_card[1]:
                        if self.noTrumpsOrder[card[0]] > self.noTrumpsOrder[best_card[0]]:
                            best_card[0] = card[0]
                            winn = i
                else:
                    if trumps_in_game == 1:
                        best_card[0] = card[0]
                        best_card[1] = card[1]
                        winn = i
                    else:
                        if card.isTrump and self.TrumpsOrder[card[0]] > self.TrumpsOrder[best_card[0]]:
                            best_card[0] = card[0]
                            winn = i
        return winn
    
    def update_score(self, winner):
        if 0 in self.moves:
            return -1

        res = 0
        if self.type == "all_trumps":
            for i in range(0,4):
                if self.moves[i] != 0:
                    temp = self.moves[i].split("_")
                    res += self.TrumpsValue[temp[0]]
        elif self.type == "no_trumps":
            for i in range(0,4):
                if self.moves[i] != 0:
                    temp = self.moves[i].split("_")
                    res += self.noTrumpsValue[temp[0]]
        else:
            pass
        
        if winner % 2 == 0:
            self.t1_score += res
        else:
            self.t2_score += res

    def eval_winner(self):
        if 0 in self.moves:
            return -1

        winn = -1
        if self.type == "all_trumps":
            winn = self.all_trumps()
        elif self.type == "no_trumps":
            winn = self.no_trumps()
        else:
            winn = self.suit_trump()

        self.turn = winn
        return winn

    def check_for_allTrumps(self, move, player):
        pass

    def check_for_noTrumps(self, move, player):
        turns_made = 4 - self.moves.count(0)
        if turns_made == 0:
            return True
        first_card = self.moves[(4 + self.turn - turns_made) % 4]
        first_card_suit = first_card.split("_")[1]
        card_suit = move.split("_")[1]

        if player.has_suit(first_card_suit):
            if card_suit != first_card_suit:
                return False

        return True

    def check_for_suit_Trump(self, move, player):
        pass

    def check_move(self, move, player):
        if self.type == "all_trumps":
            return self.check_for_allTrumps(move, player)

        if self.type == "no_trumps":
            return self.check_for_noTrumps(move, player)

        if self.type == "suit_trump":
            return self.check_for_suit_Trump(move, player)

    def reset_moves(self): # resets the played action
        self.moves = [0,0,0,0]

    def get_players_number_of_cards(self):
        return self.players_number_of_cards
    
    def deal_num_cards(self, n):
        cards = []
        for i in range(0, n):
            cards.append(all_cards[self.deck[i]]) 
        return cards

   