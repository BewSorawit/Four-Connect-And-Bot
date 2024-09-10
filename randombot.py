import random
# Connect Four game in Python (console version)
ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
    return board

def print_board(board):
    for row in board:
        print(row)

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for row in range(ROW_COUNT - 1, -1, -1):
        if board[row][col] == 0:
            return row

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for a win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# Check if a player can win in the next move
def check_for_winning_move(board, piece):
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            temp_board = [r[:] for r in board]  # Create a copy of the board
            drop_piece(temp_board, row, col, piece)
            if winning_move(temp_board, piece):
                return col
    return None

# Bot move with both attack and defense strategy
def bot_move(board, bot_piece, player_piece):
    # Check if the bot can win on the next move
    col_to_win = check_for_winning_move(board, bot_piece)
    if col_to_win is not None:
        return col_to_win

    # Check if the player can win on the next move, and block it
    col_to_block = check_for_winning_move(board, player_piece)
    if col_to_block is not None:
        return col_to_block

    # Otherwise, choose a random valid column
    valid_columns = [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]
    return random.choice(valid_columns)

def main():
    board = create_board()
    game_over = False
    turn = 0  # 0 for player, 1 for bot

    print_board(board)
    while not game_over:
        #print_board(board)
        
        # Player 1 Input
        if turn == 0:
            col = int(input("Player 1, make your selection (0-6): "))
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                # Show the latest board
                print_board(board)

                if winning_move(board, 1):
                    print("Player 1 wins!")
                    game_over = True

        # Bot move
        else:
            print("Bot is making a move...")
            col = bot_move(board, 2, 1)  # Bot is piece 2, player is piece 1
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                # Show the latest board
                print_board(board)

                if winning_move(board, 2):
                    print("Bot wins!")
                    game_over = True

        turn += 1
        turn = turn % 2

if __name__ == "__main__":
    main()
