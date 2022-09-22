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
        self.type = "no_trumps"
        self.trump = ""
        _deck = random.shuffle(card_keys)

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
        pass
    
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

    def reset_moves(self): # resets the played action
        self.moves = [0,0,0,0]

    def get_players_number_of_cards(self):
        return self.players_number_of_cards
    
    def deal_num_cards(n):
        random.shuffle(card_keys)
        cards = []
        for i in range(0, n):
            cards.append(all_cards[card_keys[0]]) 
            card_keys.pop(0)
        return cards

    def deal_cards(players,deck,number_of_cards):
        player_index=0
        for i in range(number_of_cards*4):
            if i%number_of_cards == 0 and i!=0:
                player_index+=1
            players[player_index].get_card(deck[0])
            del deck[0]

    def play_game(players,cards_on_table,first_pl,type):
        winner=0
        points=0
        for i in range(4):
            card=0
            print(players[first_pl+i%4].cards[card].suit,players[first_pl+i%4].cards[card].number)
            if players[first_pl+i%4].cards[card].number==14:
                if type==1 or players[first_pl+i%4].cards[card].suit==type:
                    players[first_pl%4].cards[card].number=12
                points+=11
            elif players[first_pl+i%4].cards[card].number==13:
                if type==1 or players[first_pl+i%4].cards[card].suit==type:
                        players[first_pl%4].cards[card].number=11
                points+=10
            elif players[first_pl+i%4].cards[card].number==12:
                if type==1 or players[first_pl+i%4].cards[card].suit==type:
                    players[first_pl%4].cards[card].number=10
                points+=4
            elif players[first_pl+i%4].cards[card].number==11:
                if type==1 or players[first_pl+i%4].cards[card].suit==type:
                    players[first_pl%4].cards[card].number=9
                points+=3
            elif players[first_pl%4].cards[card].number==10:
                if type==1 or players[first_pl+i%4].cards[card].suit==type:
                    players[first_pl%4].cards[card].number=14
                    points+=20
                else: 
                    points+=2
            elif players[first_pl%4].cards[card].number==9:
                if type==1 or players[first_pl+i%4].cards[card].suit==type:
                    players[first_pl%4].cards[card].number=13
                    points+=14
            players[(first_pl+i)%4].play_turn(card,cards_on_table)
            if cards_on_table[i].suit==type and cards_on_table[winner].suit!=type:
                winner=(first_pl+i)%4
            if cards_on_table[i].number>cards_on_table[winner].number and cards_on_table[i].suit==cards_on_table[winner].suit:
                winner=(first_pl+i)%4
            
        return points*10+winner