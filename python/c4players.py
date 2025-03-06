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
        self.NUMCOLS = c4model.NUMROWS # 7

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
    
    def utility(self, board_state):
        terminal_status = self.terminal_test(board_state) # Returns 1 if theres a winner, 0 if theres a draw, and -1 if the games not over
        if terminal_status == 1: # There's a winner
            return 1000
        elif terminal_status == 0: # There's a draw
            return 0
        elif terminal_status == -1: # Games not over
            return -1000
        else:
            print("We shouldnt have gotten here! There's some error in the code, go fix it please")
            
    
    # Returns 0 if theres a winner, 1 if theres a draw, and -1 if the games not over
    def terminal_test(self, board_state):

        if self.check_for_win(board_state): 
            return 1
        elif self.check_for_draw(board_state):
            return 0
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
    
    
    # Helper functions

    def check_for_draw(self, board_state): # This functions assumes that the given state is valid
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
            print("It's players2's turn")
            return self.PLAYER2
        elif player2_piece_count == player1_piece_count:
            print("It's players1's turn")
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
                f"Invalid input: {player}! option's are player1, represented as: {self.PLAYER1}, or player2, represented as: {self.PLAYER2}"
            )
