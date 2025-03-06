import math
import c4players

# Sample board states
board_states = [
    [  # Board state 1: A near-complete board with no winner yet
        [-1, 1, -1, 1, -1, 2, -1],
        [-1, 2, -1, 1, -1, 2, -1],
        [-1, 2, -1, 1, 1, 1, -1],
        [2, 2, -1, 2, 2, 1, 1],
        [1, 1, -1, 2, 1, 2, 2],
        [1, 2, 2, 1, 1, 2, 1]
    ]
]


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
        print(f"\nTesting board state {iteration}:")
        print_board(state)
        
        # Test specific functions
        # test_valid_actions(ai_player, state)
        # test_result(ai_player, 4, state)
        # test_utility(ai_player, state)
        test_terminal_test(ai_player, state)
        # test_alpha_beta_search(ai_player, state)

# Functions to test individual functions in ConnectFourAIPlayer
def test_valid_actions(ai_player, board_state):
    print("\nTesting valid_actions function:")
    actions = ai_player.valid_actions(board_state)
    print(actions)

def test_result(ai_player, action, board_state):
    print("\nTesting result function (example with action in column 3):")
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

# Function to print the board state
def print_board(board_state):
    for row in (board_state):
        print(row)

# Now let's test the AI with the provided board states
for board_state in board_states:
    model = ConnectFourModel(board_state)
    debut_ai(model, [board_state])
