import random
import math


class ConnectFourPlayer:
    def get_move(self):
        # Must return a value between 0 and 6 (inclusive), where 0 is the left-most column and 6 is the right-most column.
        raise NotImplementedError('Must be implemented by subclass')

    def is_automated(self):
        # AI players should return True, human players should return False
        return True


class ConnectFourHumanPlayer(ConnectFourPlayer):
    def __init__(self, model):
        self.model = model

    def is_automated(self):
        return False

    def get_move(self):
        valid_input = False
        valid_columns = self.model.get_valid_moves()

        while not valid_input:
            try:
                column = int(input('Enter column (1-7): '))
                if column < 1 or column > 7:
                    raise ValueError()
                else:
                    valid_input = True

                if valid_columns[column-1]:
                    return column-1
                else:
                    print('That column is full. Pick again.')
                    valid_input = False
            except ValueError:
                print('Invalid input.')

        # Should not get here
        return -1
    

class ConnectFourRandomPlayer(ConnectFourPlayer):
    def __init__(self, model):
        self.model = model

    def get_move(self):
        moves = self.model.get_valid_moves()
        m = random.randrange(7)
        while not moves[m]:
            m = random.randrange(7)
        return m

# Constant variable used by AI Player

PLAYER1 = 1
PLAYER2 = 2
EMPTY = -1

NUMCOLS = 7
NUMROWS = 6

class ConnectFourAIPlayer(ConnectFourPlayer):
    def __init__(self, model):
        self.model = model

    # Currently our AI choses the move closest to the left
    def get_move(self):
        # Replace the following code with an alpha beta pruning algorithm
        m = self.alpha_beta_search(self.model.get_grid())
        return m
        """ OLD CODE, LEFT FIRST
        moves = self.model.get_valid_moves()
        m = 0
        while not moves[m]:
            m += 1
        return m
        """
    
    def valid_actions(self, board_state):
    
        return [(board_state[x][0] == EMPTY) for x in range(NUMCOLS)]
    
    def result(self, action, board_state):

        board_state_copy = [row for row in board_state]
        current_player = self.get_current_player()

        # Loop through the rows in reverse order, starting from the last/bottom row (NUMROWS - 1) to the first/top row (0)
        for row in range(NUMROWS - 1, -1, -1):
            if board_state_copy[row][action] == EMPTY:
                board_state_copy[row][action] = current_player
                return board_state_copy

        raise ValueError(f"Column {action} is full!")  # Handle full column case
    
    
    # Alpha beta functions
    
    def utility(self, board_state):
        terminal_status = self.terminal_test(board_state) # Returns 0 if theres a winner, 1 if theres a draw, and -1 if the games not over
        if terminal_status == 0: # There's a winner
            return 1000
        elif terminal_status == 1: # There's a draw
            return 0
        elif terminal_status == -1: # Games not over
            return -1000
        else:
            print("We shouldnt have gotten here! There's some error in the code, go fix it please")
            
    
    # Returns 0 if theres a winner, 1 if theres a draw, and -1 if the games not over
    def terminal_test(self, board_state):
        
        # This functions assumes that the given state is valid
        def theres_a_draw():
            for i in range(NUMCOLS):
                if board_state[i][0] == EMPTY:
                        return False
            return True

        if self.check_for_win(): # Calculate who we are and pass it in
            return 0
        elif theres_a_draw():
            return 1
        else:
            return -1

    def alpha_beta_search(self,board_state):
        output = self.max_value(board_state, -1000, 1000)
        return output[1]
    
    def max_value(self,board_state, alpha, beta):
        if self.utility(board_state) != -1000:
            return (self.utility(board_state), None)
        v = -math.inf
        for a in self.valid_actions(board_state):
            (v2,a2) = self.min_value(self.result(board_state,a),alpha,beta)
            if v2 > v:
                (v,move) = v2,a
                alpha = max(alpha, v)
            if v >= beta:
                return (v, move)
        return (v,move)
    
    def min_value(self,board_state, alpha, beta):
        if self.utility(board_state) != -1000:
            return self.utility(board_state), None
        v = math.inf
        for a in self.valid_actions(board_state):
            (v2,a2) = self.max_value(self.result(board_state,a),alpha,beta)
            if v2 < v:
                (v,move) = v2,a
                beta = min(beta, v)
            if v <= alpha:
                return (v, move)
        return (v,move)
    
    
    # Helper functions

    def check_for_win(player, board_state): # options are PLAYER1, PLAYER2, or ANY

        def horizontal_win():
            win = False
            for row in range(NUMROWS):
                for col in range(4):
                    if board_state[col][row] != EMPTY:
                        win = (board_state[col][row] == board_state[col + 1][row]) and (
                            board_state[col][row] == board_state[col + 2][row]) and (
                                board_state[col][row] == board_state[col + 3][row])
                    if win:
                        return True
            return False

        def vertical_win():
            win = False
            for col in range(NUMCOLS):
                for row in range(3):
                    if board_state[col][row] != EMPTY:
                        win = (board_state[col][row] == board_state[col][row + 1]) and (
                            board_state[col][row] == board_state[col][row + 2]) and (
                                board_state[col][row] == board_state[col][row + 3])
                    if win:
                        return True
            return False

        def neg_diagonal_win():
            win = False
            for col in range(4):
                for row in range(3):
                    if board_state[col][row] != EMPTY:
                        win = (board_state[col][row] == board_state[col + 1][row + 1]) and (
                            board_state[col][row] == board_state[col + 2][row + 2]) and (
                                board_state[col][row] == board_state[col + 3][row + 3])
                    if win:
                        return True
            return False

        def pos_diagonal_win():
            win = False
            for col in range(3, 7):
                for row in range(3):
                    if board_state[col][row] != EMPTY:
                        win = (board_state[col][row] == board_state[col - 1][row + 1]) and (
                            board_state[col][row] == board_state[col - 2][row + 2]) and (
                                board_state[col][row] == board_state[col - 3][row + 3])
                    if win:
                        return True
            return False
        
        return (horizontal_win() or
                    vertical_win() or
                    neg_diagonal_win() or
                    pos_diagonal_win()) 


    def get_current_player(board_state):
        
        player1_piece_count = sum(row.count(1) for row in board_state)
        player2_piece_count = sum(row.count(2) for row in board_state)

        if player2_piece_count < player1_piece_count:
            return PLAYER2
        elif player2_piece_count == player1_piece_count:
            return PLAYER1
        else:
            raise ValueError(
                f"Invalid board state! player1: {player1_piece_count}, player2: {player2_piece_count}"
            )

