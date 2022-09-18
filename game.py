class Game:
    def __init__(self, id):
        self.id = id
        self.t1_score = 0
        self.t2_score = 0
        self.moves = [0,0,0,0]
        self.turn = 0

    def get_moves(self):
        return self.moves

    def get_player_move(self, player):
        pass

    def make_move(self, player, move):
        self.moves[player] = move
        self.turn = (self.turn + 1) % 4

    def connected(self):
        pass

    def both_played(self):
        pass

    def winner(self):
        pass

    def reset_moves(self): # resets the played action
        pass