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

def main():
    board = create_board()
    game_over = False
    turn = 0

    while not game_over:
        print_board(board)
        
        # Player 1 Input
        if turn == 0:
            col = int(input("Player 1, make your selection (0-6): "))
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    print("Player 1 wins!")
                    game_over = True

        # Player 2 Input
        else:
            col = int(input("Player 2, make your selection (0-6): "))
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    print("Player 2 wins!")
                    game_over = True

        turn += 1
        turn = turn % 2

if __name__ == "__main__":
    main()
