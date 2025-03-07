import random
import math
import c4model


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
    

class ConnectFourAIPlayer(ConnectFourPlayer):

    def __init__(self, model):
        self.model = model
        self.initialize_game_specifications()

    def initialize_game_specifications(self):
        # Set up for connect four (this setup will be different in tic tac toe)
        self.PLAYER1 = c4model.PLAYER1 # 1
        self.PLAYER2 = c4model.PLAYER2 # 2
        self.EMPTY = c4model.EMPTY # -1

        self.NUMROWS = c4model.NUMROWS # 6
        self.NUMCOLS = c4model.NUMCOLS # 7

    def get_move(self):
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
        return [x for x in range(self.NUMCOLS) if board_state[x][0] == self.EMPTY]

    
    def result(self, action, board_state): 
        # Perform a **deep copy** of the board
        board_state_copy = [col[:] for col in board_state]  # Copy each column separately
        
        current_player = self.get_current_player(board_state)

        # Start from the lowest row (bottom of the column) and move upward
        for row in range(self.NUMROWS - 1, -1, -1):  # Iterate from bottom (5) to top (0)
            if board_state_copy[action][row] == self.EMPTY:  # Check if the slot is empty
                board_state_copy[action][row] = current_player  # Drop the piece
                return board_state_copy  # Return the updated board state

        raise ValueError(f"Column {action} is full!")  # No empty slots
            

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
    
    def min_value(self, board_state, alpha, beta):
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
    
        
    def utility(self, board_state):
        
        if self.check_for_win(board_state):
            return 1000 # There's a win!
        elif self.check_for_full_board(board_state):
            return 0 # Theres a draw (A full board without a win is a draw)
        else: 
            return -1000 # The game isn't over

    
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
    
    # This function isn't isnt fully ready, 
    # The check_for_win function  needs to be ammended to check for a win from a specific player
    # It currently checks for any win.
    def mid_game_utility(self, board_state, our_piece, enemy_piece):

        # First check if the games over:

        max_utility = 492 # This is the score when the board is completely filled with our pieces
        min_utility = -492 # This is the score when the board is completely filled with the opponent’s pieces     

        if self.check_for_win(board_state, our_piece):
            return max_utility
        elif self.check_for_win(board_state, enemy_piece): 
            return min_utility
        elif self.check_for_full_board(board_state): 
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
    
    # Returns 0 if theres a winner, 1 if theres a draw, and -1 if the games not over
    def terminal_test(self, board_state):

        if self.check_for_win(board_state): 
            return 1
        elif self.check_for_full_board(board_state):
            return 0
        else:
            return -1

    def check_for_full_board(self, board_state): # This functions assumes that the given state is valid
        for i in range(self.NUMCOLS):
            if board_state[i][0] == self.EMPTY:
                    return False
        return True
    

    def check_for_win(self, board_state, player="any"): # options are self.PLAYER1, self.PLAYER2, or if no player is provided we check if there is any winner

        def horizontal_win():
            win = False
            for row in range(self.NUMROWS):
                for col in range(4):
                    if board_state[col][row] != self.EMPTY:
                        win = (board_state[col][row] == board_state[col + 1][row]) and (
                            board_state[col][row] == board_state[col + 2][row]) and (
                                board_state[col][row] == board_state[col + 3][row])
                    if win:
                        return True
            return False

        def vertical_win():
            win = False
            for col in range(self.NUMCOLS):
                for row in range(3):
                    if board_state[col][row] != self.EMPTY:
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
                    if board_state[col][row] != self.EMPTY:
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
                    if board_state[col][row] != self.EMPTY:
                        win = (board_state[col][row] == board_state[col - 1][row + 1]) and (
                            board_state[col][row] == board_state[col - 2][row + 2]) and (
                                board_state[col][row] == board_state[col - 3][row + 3])
                    if win:
                        return True
            return False

        return (horizontal_win() 
                or vertical_win() 
                or neg_diagonal_win() 
                or pos_diagonal_win()) 


    def get_current_player(self, board_state):
        
        player1_piece_count = sum(row.count(1) for row in board_state)
        player2_piece_count = sum(row.count(2) for row in board_state)

        if player2_piece_count < player1_piece_count:
            # print("It's players2's turn")
            return self.PLAYER2
        elif player2_piece_count == player1_piece_count:
            # print("It's players1's turn")
            return self.PLAYER1
        else:
            raise ValueError(
                f"Invalid board state! player1: {player1_piece_count}, player2: {player2_piece_count}"
            )
        
    def other_player(self, player):

        if player == self.PLAYER1:
            return self.PLAYER2
        
        elif player == self.PLAYER2:
            return self.PLAYER1
        
        else:
            raise ValueError(
                f"Invalid input: {player}! option's are PLAYER1, represented as: {self.PLAYER1}, or PLAYER2, represented as: {self.PLAYER2}"
            )
