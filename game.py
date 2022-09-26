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
    all_cards[key] = Card(0,0,card_name, card_suit, False)

class Game:
    def __init__(self, id):
        self.id = id
        self.playing = False
        self.t1_score = 0
        self.t2_score = 0
        self.moves = [0,0,0,0]
        self.players_number_of_cards = [0,0,0,0]
        self.turn = 0
        self.deal_turn = 0
        self.change_type_turn = 0
        self.types_calls = [0,0,0,0]
        self.score_multiplier = 1
        

        self.type = ""
        self.trump = ""
        self.deal = True
        self.deck = card_keys
        random.shuffle(self.deck)
        self.noTrumpsOrder = {"seven" : 0, "eight": 1, "nine" : 2, "jack": 3, "queen": 4, "king": 5, "ten": 6, "ace": 7}
        self.TrumpsOrder = {"seven" : 0, "eight": 1, "queen": 2, "king": 3, "ten": 4, "ace": 5, "nine" : 6, "jack": 7}

        self.noTrumpsValue = {"seven" : 0, "eight": 0, "nine" : 0, "jack": 2, "queen": 3, "king": 4, "ten": 10, "ace": 11}
        self.TrumpsValue = {"seven" : 0, "eight": 0, "queen": 3, "king": 4, "ten": 10, "ace": 11, "nine" : 14, "jack": 20}
        self.gameTypes = {"clubs": 0, "diamonds": 1, "hearts": 2, "spades": 3, "no_trumps": 4, "all_trumps": 5}

    def get_moves(self):
        return self.moves

    def ended(self):
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

    def change_trump(self, suit):
        self.trump = suit
        for card in self.deck:
            all_cards[card].isTrump = True

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

    def reset_deck(self):
        self.deck = card_keys
        random.shuffle(self.deck)

    def get_players_number_of_cards(self):
        return self.players_number_of_cards
    
    def deal_num_cards(self, n):
        cards = []
        for i in range(0, n):
            cards.append(all_cards[self.deck[i]]) 
        return cards

    def can_call_game_type(self, game_type):
        if game_type == "pass":
            return True
        if self.type == "":
            if game_type == "2x" or game_type == "4x":
                return False
            return True
        
        if game_type == "2x":
            if self.score_multiplier == 1:
                return True
            else:
                return False
        if game_type == "4x":
            if self.score_multiplier == 2:
                return True
            else:
                return False

        if self.gameTypes[game_type] <= self.gameTypes[self.type]:
            return False

        return True
   