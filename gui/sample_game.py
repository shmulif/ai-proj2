def parse_turns(input_str):
    # Split the input string into turns based on 'Current turn' separator
    turns = input_str.split('Current turn:')
    
    board_list = []
    
    for turn in turns[1:]:  # Skip the first empty element due to split
        # Extract the board, which is between the 'Current turn' and the next
        # 'Current turn' or end of the string
        board_str = turn.strip().split('\n')[1:]  # Remove the "Current turn" label and empty line
        board = []

        for row in board_str:
            board.append([cell if cell != '-' else '-' for cell in row.split()])
        
        board_list.append(board)
    
    return board_list

# Example usage:
input_str = """- - - - - - -
- - - - - - -
- - - - - - -
- - - - - - -
- - - - - - -
- - - - - - -

Current turn: PLAYER 1
- - - - - - - 
- - - - - - - 
- - - - - - - 
- - - - - - - 
- - - - - - - 
- - X - - - - 

Current turn: PLAYER 2
- - - - - - - 
- - - - - - - 
- - - - - - - 
- - - - - - - 
- - O - - - - 
- - X - - - - 

Current turn: PLAYER 1
- - - - - - - 
- - - - - - - 
- - - - - - - 
- - - - - - - 
- - O - - - - 
- - X - - X - 

Current turn: PLAYER 2
- - - - - - - 
- - - - - - - 
- - - - - - - 
- - - - - - - 
- - O - - O - 
- - X - - X - 

Current turn: PLAYER 1
- - - - - - - 
- - - - - - - 
- - - - - - - 
- - X - - - - 
- - O - - O - 
- - X - - X - 

Current turn: PLAYER 2
- - - - - - - 
- - - - - - - 
- - - - - - - 
- - X - - - - 
- - O - - O - 
- - X O - X - 

Current turn: PLAYER 1
- - - - - - - 
- - - - - - - 
- - - - - - - 
- - X - - - - 
- - O - - O - 
- - X O - X X 

Current turn: PLAYER 2
- - - - - - - 
- - - - - - - 
- - - - - - - 
- - X - - - - 
- - O - - O - 
- - X O O X X 

Current turn: PLAYER 1
- - - - - - - 
- - - - - - - 
- - X - - - - 
- - X - - - - 
- - O - - O - 
- - X O O X X 

Current turn: PLAYER 2
- - - - - - - 
- - - - - - - 
- - X - - - - 
- - X - - - - 
- - O - - O O 
- - X O O X X 

Current turn: PLAYER 1
- - - - - - - 
- - - - - - - 
- - X - - - - 
- - X - - - X 
- - O - - O O 
- - X O O X X 

Current turn: PLAYER 2
- - - - - - - 
- - - - - - - 
- - X - - - O 
- - X - - - X 
- - O - - O O 
- - X O O X X 

Current turn: PLAYER 1
- - - - - - - 
- - - - - - - 
- - X - - - O 
- - X - - - X 
- - O X - O O 
- - X O O X X 

Current turn: PLAYER 2
- - - - - - - 
- - - - - - - 
- - X - - - O 
- - X - - - X 
- - O X - O O 
O - X O O X X 

Current turn: PLAYER 1
- - - - - - - 
- - - - - - - 
- - X - - - O 
- - X - - - X 
- - O X - O O 
O X X O O X X 

Current turn: PLAYER 2
- - - - - - - 
- - - - - - O 
- - X - - - O 
- - X - - - X 
- - O X - O O 
O X X O O X X 

Current turn: PLAYER 1
- - - - - - - 
- - - - - - O 
- - X - - - O 
- - X - - - X 
- - O X X O O 
O X X O O X X 

Current turn: PLAYER 2
- - - - - - - 
- - - - - - O 
- - X - - - O 
- - X - - - X 
O - O X X O O 
O X X O O X X 

Current turn: PLAYER 1
- - - - - - - 
- - - - - - O 
- - X - - - O 
X - X - - - X 
O - O X X O O 
O X X O O X X 

Current turn: PLAYER 2
- - - - - - O 
- - - - - - O 
- - X - - - O 
X - X - - - X 
O - O X X O O 
O X X O O X X 

Current turn: PLAYER 1
- - - - - - O 
- - - - - - O 
- - X - - - O 
X - X - X - X 
O - O X X O O 
O X X O O X X 

Current turn: PLAYER 2
- - - - - - O 
- - O - - - O 
- - X - - - O 
X - X - X - X 
O - O X X O O 
O X X O O X X 

Current turn: PLAYER 1
- - - - - - O 
- - O - - - O 
X - X - - - O 
X - X - X - X 
O - O X X O O 
O X X O O X X 

Current turn: PLAYER 2
- - - - - - O 
- - O - - - O 
X - X - O - O 
X - X - X - X 
O - O X X O O 
O X X O O X X 

Current turn: PLAYER 1
- - - - - - O 
- - O - - - O 
X - X - O - O 
X - X - X - X 
O X O X X O O 
O X X O O X X 

Current turn: PLAYER 2
- - - - - - O 
- - O - O - O 
X - X - O - O 
X - X - X - X 
O X O X X O O 
O X X O O X X 

Current turn: PLAYER 1
- - - - - - O 
- - O - O - O 
X - X - O - O 
X - X - X X X 
O X O X X O O 
O X X O O X X 

Current turn: PLAYER 2
- - - - - - O 
O - O - O - O 
X - X - O - O 
X - X - X X X 
O X O X X O O 
O X X O O X X 

Current turn: PLAYER 1
X - - - - - O 
O - O - O - O 
X - X - O - O 
X - X - X X X 
O X O X X O O 
O X X O O X X 

Current turn: PLAYER 2
X - - - - - O 
O - O - O - O 
X - X - O - O 
X O X - X X X 
O X O X X O O 
O X X O O X X 

Current turn: PLAYER 1
X - - - - - O 
O - O - O - O 
X - X - O X O 
X O X - X X X 
O X O X X O O 
O X X O O X X"""  # Input the full board string here

# turns = parse_turns(input_str)

# # Get the first turn's board (index 0)
# first_turn_board = turns[1]

# # Iterate through the board
# for row in first_turn_board:
#     for entry in row:
#         print(entry)

print(input_str)