import copy
import math


class TicTacToeHumanPlayer:
    def __init__(self, model, symbol):
        self.model = model
        self.symbol = symbol

    def is_automated(self):
        return False

    def get_move(self):
        valid_input = False
        valid_moves = self.model.get_valid_moves()

        while not valid_input:
            try:
                move = int(input('Enter move (1-9): '))
                if move < 1 or move > 9:
                    raise ValueError()
                else:
                    valid_input = True

                if move in valid_moves:
                    return move
                else:
                    print('That spot is full. Pick again.')
                    valid_input = False
            except ValueError:
                print('Invalid input.')

        # Should not get here
        return -1


class TicTacToeAIPlayer:
    def __init__(self, model, symbol):
        self.model = model
        self.symbol = symbol
        self.initialize_game_specifications()

    def initialize_game_specifications(self):
        # Set up for tic tac toe
        self.PLAYER1 = 1
        self.PLAYER2 = 2
        self.EMPTY = None

        self.NUMROWS = 3
        self.NUMCOLS = 3

    def is_automated(self):
        return True

    # Assume actions are numbered 1-9
    def result(self, action, state):
        newstate = copy.deepcopy(state)
        turn = self._get_turn(state)

        action -= 1 # Adjustment of 1
        col = action % 3
        row = action // 3
        newstate[row][col] = turn

        return newstate

    def actions(self, state):
        moves = []
        for row in range(3):
            for col in range(3):
                if state[row][col] is None:
                    moves.append(row*3 + col + 1)
        return moves

    def terminal_test(self, state):
        for row in range(3):
            if state[row][0] is not None and state[row][0] == state[row][1] and state[row][0] == state[row][2]:
                return True
        for col in range(3):
            if state[0][col] is not None and state[0][col] == state[1][col] and state[0][col] == state[2][col]:
                return True
        if state[0][0] is not None and state[0][0] == state[1][1] and state[0][0] == state[2][2]:
            return True
        if state[2][0] is not None and state[2][0] == state[1][1] and state[2][0] == state[0][2]:
            return True

        return self._is_draw(state)

    def utility(self, state):
        if self._get_winner(state) == self.symbol:
            return 1000
        elif self._get_winner(state) is not None:
            return -1000
        if self._is_draw(state):
            return 0

        return 0 # Should not happen

    def _is_draw(self, state):
        all_filled = True
        for row in range(3):
            for col in range(3):
                if state[row][col] is None:
                    all_filled = False
        return all_filled

    def _get_winner(self, state):
        for row in range(3):
            if state[row][0] is not None and state[row][0] == state[row][1] and state[row][0] == state[row][2]:
                return state[row][0]
        for col in range(3):
            if state[0][col] is not None and state[0][col] == state[1][col] and state[0][col] == state[2][col]:
                return state[0][col]
        if state[0][0] is not None and state[0][0] == state[1][1] and state[0][0] == state[2][2]:
            return state[0][0]
        if state[2][0] is not None and state[2][0] == state[1][1] and state[2][0] == state[0][2]:
            return state[2][0]

        return None # Uh-oh

    def _get_turn(self, state):
        empties = 0
        for row in range(3):
            for col in range(3):
                if state[row][col] is None:
                    empties += 1

        if empties % 2 == 1:
            return 'X'
        else:
            return 'O'

    def get_move(self):
        m = self.alpha_beta_search(self.model.get_grid(), 9) # 9 is the max amount of turns in tic tac toe
        return m

    def alpha_beta_search(self, board_state, depth):
        output = self.max_value(board_state, -1000, 1000, depth)
        return output[1]

    def max_value(self, board_state, alpha, beta, depth):
        if self.utility(board_state) == -1000 or depth <= 0:
            return (self.utility(board_state), None)
        v = -math.inf
        if not self.actions(board_state): # Added this to get rid of an error
            return (0,-1)
        for a in self.actions(board_state):
            (v2,a2) = self.min_value(self.result(a,board_state),alpha,beta, depth - 1)
            if v2 > v:
                (v,move) = v2,a
                alpha = max(alpha, v)
            if v >= beta:
                return (v, move)
        return (v,move)

    def min_value(self, board_state, alpha, beta, depth):
        if self.utility(board_state) == -1000 or depth <= 0:
            return self.utility(board_state), None
        v = math.inf
        if not self.actions(board_state): # Added this to get rid of an error
            return (0,-1)
        for a in self.actions(board_state):
            (v2,a2) = self.max_value(self.result(a,board_state),alpha,beta, depth-1)
            if v2 < v:
                (v,move) = v2,a
                beta = min(beta, v)
            if v <= alpha:
                return (v, move)
        return (v,move)
    
    """
    In this method we check for a potential 
    win in each of these eight directions:

              N
              ↑
       NW  ↖  |  ↗  NE
            \ | /
    W  ← - - - - - - →  E
            / | \
       SW  ↙  |  ↘  SE
              ↓
              S
            
    """
    
    def mid_game_utility(self, board_state, our_piece, enemy_piece):

        # First check if the games over:

        max_utility = 492 # This is the score when the board is completely filled with our pieces
        min_utility = -492 # This is the score when the board is completely filled with the opponent’s pieces     

        if self.check_for_win(board_state, our_piece):
            return max_utility
        elif self.check_for_win(board_state, enemy_piece): 
            return min_utility
        elif self._is_draw(board_state): 
            return 0 # Theres a draw (A full board without a win is a draw)
        
        # If the games not over, proceed to claculate the utility:
        score = 0
        
        # We measure utility for each piece in the grid, and add it to the total utility
        for i in range(len(board_state)):
            for j in range(len(board_state[i])):
                
                current_piece = board_state[i][j]
            
                if current_piece == our_piece or current_piece == self.EMPTY:
                    score += self.check_win_potential('N', board_state, our_piece, i, j)
                    score += self.check_win_potential('NE', board_state, our_piece, i, j)
                    score += self.check_win_potential('E', board_state, our_piece, i, j)
                    score += self.check_win_potential('SE', board_state, our_piece, i, j)
                    score += self.check_win_potential('S', board_state, our_piece, i, j)
                    score += self.check_win_potential('SW', board_state, our_piece, i, j)
                    score += self.check_win_potential('W', board_state, our_piece, i, j)
                    score += self.check_win_potential('NW', board_state, our_piece, i, j)
                
                else: # If the peice is the enemy's piece, subtract the
                    score -= self.check_win_potential('N', board_state, enemy_piece, i, j)
                    score -= self.check_win_potential('NE', board_state, enemy_piece, i, j)
                    score -= self.check_win_potential('E', board_state, enemy_piece, i, j)
                    score -= self.check_win_potential('SE', board_state, enemy_piece, i, j)
                    score -= self.check_win_potential('S', board_state, enemy_piece, i, j)
                    score -= self.check_win_potential('SW', board_state, enemy_piece, i, j)
                    score -= self.check_win_potential('W', board_state, enemy_piece, i, j)
                    score -= self.check_win_potential('NW', board_state, enemy_piece, i, j)
            
            
        return score
            
    """
    Returns a number from -1 to 3
    -1 means we can't get a win in this direction (we loose a point)
    0 means we could get a win
    1 means we could get a win and we already have 1 of the pieces
    2 means we could get a win and we already have 2 of the pieces
    3 means we could get a win and we already have 3 of the pieces
    """
    def check_win_potential(self, direction, board_state, our_piece,  i, j):
                
        sub_score = 1 # If the four spots are open, this amount will not get updated
        
        if direction == 'N':
            step_col = 0 # Stay in the same column
            step_row = -1 # Go towards the top (beggining) of the column
        elif direction == 'NE':
            step_col = 1 # Go to the next column
            step_row = -1 # Go towards the top (beggining) of the column
        elif direction == 'E':
            step_col = 1 # Go to the next column
            step_row = 0 # Stay at the same level in the column
        elif direction == 'SE':
            step_col = 1 # Go to the next column
            step_row = 1 # Go towards the bottom (end) of the column
        elif direction == 'S':
            step_col = 0 # Stay in the same column
            step_row = 1 # Go towards the bottom (end) of the column
        elif direction == 'SW':
            step_col = -1 # Go to the previous column
            step_row = 1 # Go towards the bottom (end) of the column
        elif direction == 'W':
            step_col = -1 # Go to the previous column
            step_row = 0 # Stay at the same level in the column
        elif direction == 'NW':
            step_col = -1 # Go to the previous column
            step_row = -1 # Go towards the top (beggining) of the column
            
        for k in range(4):
        
            col_index = i + (k * step_col)
            row_index = j + (k * step_row)

            if not self.in_board_range(col_index, row_index):
                return -1 # There aren't three more spots on the board in that direction
            else:
                piece = board_state[col_index][row_index]
                if piece == our_piece:
                    sub_score += 1
                elif piece == self.EMPTY:
                    continue
                else:
                    return -1 # There's an enemy's piece blocking us
                                
        return sub_score



    def in_board_range(self, col_index, row_index):
        return (-1 < col_index and col_index < self.NUMCOLS 
            and -1 < row_index and row_index < self.NUMROWS)
    
    # # Returns 0 if theres a winner, 1 if theres a draw, and -1 if the games not over
    # def terminal_test(self, board_state):

    #     if self.check_for_win(board_state): 
    #         return 1
    #     elif self._is_draw(board_state):
    #         return 0
    #     else:
    #         return -1
    

    def check_for_win(self, state, player="any"): # options are self.PLAYER1, self.PLAYER2, or if no player is provided we check if there is any winner
        
        for row in range(3):
            if player == "any":
                if state[row][0] is not None and state[row][0] == state[row][1] and state[row][0] == state[row][2]:
                    return True
            else:
                if state[row][0] == player and state[row][0] == state[row][1] and state[row][0] == state[row][2]:
                    return True

        for col in range(3):
            if player == "any":
                if state[0][col] is not None and state[0][col] == state[1][col] and state[0][col] == state[2][col]:
                    return True
            else:
                if state[0][col] == player and state[0][col] == state[1][col] and state[0][col] == state[2][col]:
                    return True
        
        if player == "any":
            if state[0][0] is not None and state[0][0] == state[1][1] and state[0][0] == state[2][2]:
                return True
            if state[2][0] is not None and state[2][0] == state[1][1] and state[2][0] == state[0][2]:
                return True
        else:
            if state[0][0] == player and state[0][0] == state[1][1] and state[0][0] == state[2][2]:
                return True
            if state[2][0] == player and state[2][0] == state[1][1] and state[2][0] == state[0][2]:
                return True
           
