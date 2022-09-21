import random
from card import Card

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
        _deck = random.shuffle(card_keys)

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

    def winner(self):
        pass

    def reset_moves(self): # resets the played action
        self.moves = [0,0,0,0]

    def get_players_number_of_cards(self):
        return self.players_number_of_cards

    def deal_cards(players,deck,number_of_cards):
        player_index=0
        for i in range(number_of_cards*4):
            if i%number_of_cards == 0 and i!=0:
                player_index+=1
            players[player_index].get_card(deck[0])
            del deck[0]

    def deal_num_cards(n):
        random.shuffle(card_keys)
        cards = []
        for i in range(0, n):


            cards.append(all_cards[card_keys[0]]) 
            card_keys.pop(0)
        return cards

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