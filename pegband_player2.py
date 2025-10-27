import random

class PegbandPlayer2:
    def __init__(self, name, board_length, board_width, board, num_pegs, num_rubberbands, player_color):
        self.name = "Ozzie 2"
        self.board_length = board_length
        self.board_width = board_width
        self.board = []
        self.num_pegs = num_pegs
        self.num_rubberbands = num_rubberbands
        self.player_color = player_color #1: G, first player -- 2: B, second player.
        self.peg_positions = []

    def place_pegs(self):
        # Fill this function to return your move to place a peg to the board
        while True:
            position = random.randint(0, self.board_length * self.board_width - 1)
            if self.board[position] == 0:
                break
        self.peg_positions.append(position)
        return position
    
    def place_rubberbands(self):
        # Fill this function to return your move to place your rubberbands to the pegs
        # Select 2-4 random pegs from your placed pegs to form a rubberband
        num_pegs_to_connect = random.randint(2, min(4, len(self.peg_positions)))
        temp = random.sample(self.peg_positions, num_pegs_to_connect)
        return temp