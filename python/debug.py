import math
import c4players

PLAYER1 = 1
PLAYER2 = 2
EMPTY = -1

NUMROWS = 6
NUMCOLS = 7

# Sample board states
board_states = [
    [  # Board state 1: A board with no winner yet
        [-1, -1, -1, 2, 1, 1],  
        [1, 2, 2, 2, 1, 2],  
        [-1, -1, -1, -1, -1, 2],
        [1, 1, 1, 2, 2, 1], 
        [-1, -1, 1, 2, 1, 1],  
        [2, 2, 1, 1, 2, 2],  
        [-1, -1, -1, 1, 2, 1] 
    ],
    [ # Board state 2: An empty board
        [-1, -1, -1, -1, -1, -1],  # Col 1
        [-1, -1, -1, -1, -1, -1],  # Col 2
        [-1, -1, -1, -1, -1, -1],  # Col 3
        [-1, -1, -1, -1, -1, -1],  # Col 4
        [-1, -1, -1, -1, -1, -1],  # Col 5
        [-1, -1, -1, -1, -1, -1],  # Col 6
        [-1, -1, -1, -1, -1, -1]   # Col 7
    ],
    [ # Board state 3: A draw
        [1, 2, 1, 1, 2, 1],  # Col 1
        [2, 1, 2, 2, 1, 2],  # Col 2
        [1, 2, 1, 1, 2, 1],  # Col 3
        [2, 1, 2, 2, 1, 2],  # Col 4
        [1, 2, 1, 1, 2, 1],  # Col 5
        [2, 1, 2, 2, 1, 2],  # Col 6
        [1, 2, 1, 1, 2, 1]   # Col 7
    ],
    [ # Board state 4: A (horizontal) win for player 1
        [-1, -1, -1, -1, 2, 1],  # Col 1
        [-1, -1, -1, -1, 2, 1],  # Col 2
        [-1, -1, -1, -1, -1, 1],  # Col 3
        [-1, -1, -1, -1, -1, 1],  # Col 4
        [-1, -1, -1, -1, -1, -1],  # Col 5
        [-1, -1, -1, -1, -1, -1],  # Col 6
        [-1, -1, -1, -1, -1, 2]   # Col 7
    ],
    [ # Board state 5: A (vertical) win for player 2
        [-1, -1, -1, -1, 2, 1],  # Col 1
        [-1, -1, -1, -1, 2, 1],  # Col 2
        [-1, -1, -1, -1, 1, 1],  # Col 3
        [-1, -1, -1, -1, 1, 2],  # Col 4
        [-1, -1, -1, -1, -1, 1],  # Col 5
        [-1, -1, -1, -1, -1, 1],  # Col 6
        [-1, -1, 2, 2, 2, 2]   # Col 7
    ],
    [ # Board state 6: A (pos diagonal) win for player 1 (col 1 is on the left, so this representation is flipped)
        [-1, -1, -1, -1, -1, 1],  # Col 1
        [-1, -1, -1, -1, 1, 2],  # Col 2
        [-1, -1, -1, 1, 2, 2],  # Col 3
        [-1, -1, 1, 2, 2, 1],  # Col 4
        [-1, -1, -1, -1, -1, 1],  # Col 5
        [-1, -1, -1, -1, -1, 2],  # Col 6
        [-1, -1, -1, -1, -1, -1]   # Col 7
    ],
    [ # Board state 7: A (neg diagonal) win for player 1 (col 1 is on the left, so this representation is flipped)
        [-1, -1, -1, -1, -1, 2],  # Col 1
        [-1, -1, -1, -1, -1, 2],  # Col 2
        [-1, -1, -1, -1, 2, 1],  # Col 3
        [-1, -1, 1, 1, 2, 2],  # Col 4
        [-1, -1, -1, 1, 1, 2],  # Col 5
        [-1, -1, -1, -1, 1, 2],  # Col 6
        [-1, -1, -1, -1, -1, 1]   # Col 7
    ],
    [ # Board state 8: A board with all 1s
        [1, 1, 1, 1, 1, 1],  # Col 1
        [1, 1, 1, 1, 1, 1],  # Col 2
        [1, 1, 1, 1, 1, 1],  # Col 3
        [1, 1, 1, 1, 1, 1],  # Col 4
        [1, 1, 1, 1, 1, 1],  # Col 5
        [1, 1, 1, 1, 1, 1],  # Col 6
        [1, 1, 1, 1, 1, 1]   # Col 7
    ],
    [ # Board state 9: A board with all 2s
        [2, 2, 2, 2, 2, 2],  # Col 1
        [2, 2, 2, 2, 2, 2],  # Col 2
        [2, 2, 2, 2, 2, 2],  # Col 3
        [2, 2, 2, 2, 2, 2],  # Col 4
        [2, 2, 2, 2, 2, 2],  # Col 5
        [2, 2, 2, 2, 2, 2],  # Col 6
        [2, 2, 2, 2, 2, 2]   # Col 7
    ]
]

board_state_label = [
                     'A board with no winner yet', 
                     'An empty board', 
                     'A draw', 
                     'A (horizontal) win for player 1', 
                     'A (vertical) win for player 2', 
                     'A (pos diagonal) win for player 1',
                     'A (neg diagonal) win for player 1',
                     'A board with all 1s',
                     'A board with all 2s'
                     ]


def create_empty_grid():
    new_grid = []
    for i in range(NUMCOLS):
        column = []
        for j in range(NUMROWS):
            if j != 1:
                column.append(EMPTY)
            else:
                column.append(6)
        board_states.append(column)


# Simulate running the AI with each board state
class ConnectFourModel:
    def __init__(self, grid):
        self.grid = grid

    def get_grid(self):
        return self.grid

iteration = 0
# Function to debut the AI
def debut_ai(model, board_states):
    global iteration
    
    ai_player = c4players.ConnectFourAIPlayer(model)
    
    for idx, state in enumerate(board_states):
        iteration += 1
        print(f"\nTesting board state {iteration}: " + board_state_label[iteration-1])
        print_board(state)
        
        # Test specific functions

        # test_valid_actions(ai_player, state) # Verified
        # test_result(ai_player, 2, state) # Verified
        # test_utility(ai_player, state) # Verified
        # test_terminal_test(ai_player, state) # Verified

        test_mid_game_utility(ai_player, state, 1, 2)
        # test_check_win_potential(ai_player, 'SW', state, 1, 3, 2)

        # test_alpha_beta_search(ai_player, state)


# Functions to test individual functions in ConnectFourAIPlayer
def test_valid_actions(ai_player, board_state):
    print("\nTesting valid_actions function:")
    actions = ai_player.valid_actions(board_state)
    print(actions)

def test_result(ai_player, action, board_state):
    print(f"\nTesting result function (example with action in column {action}):")
    result_state = ai_player.result(action, board_state)  # Example action in column 3
    print_board(result_state)

def test_utility(ai_player, board_state):
    print("\nTesting utility function:")
    utility = ai_player.utility(board_state)
    print(utility)

def test_terminal_test(ai_player, board_state):
    print("\nTesting terminal_test function:")
    terminal_status = ai_player.terminal_test(board_state)
    print(terminal_status)

def test_alpha_beta_search(ai_player, board_state):
    print("\nTesting alpha_beta_search function:")
    best_move = ai_player.alpha_beta_search(board_state)
    print(best_move)

def test_mid_game_utility(ai_player, board_state,  our_piece, enemy_piece):
    print("\nTesting mid_game_utility function:")
    mid_game_utility = ai_player.mid_game_utility(board_state,  our_piece, enemy_piece)
    print(mid_game_utility)

def test_check_win_potential(ai_player, direction, board_state,  our_piece, i, j):
    print("\nTesting check_win_potential function:")
    win_potential = ai_player.check_win_potential(direction, board_state,  our_piece, i, j)
    print(win_potential)

# Function to print the board state
def print_board(board_state):
    for row in (board_state):
        print(row)

# Now let's test the AI with the provided board states
for board_state in board_states:
    model = ConnectFourModel(board_state)
    debut_ai(model, [board_state])
