from random import randint

from v7bot import TicTacToe2
# DEFINE HELPER FUNCTIONS HERE IF NEEDED

# is_open: takes in the matrix for a reference, and checks if the spot at a given row and column is open
def is_open(board, row, col):
    return board[row][col] == 0

# returns None for no win, 0 for tie, 1 for bot win, and -1 for user win
# todo: complete and test
# we're gonna want test cases for this one
def has_winner(board):
    count = 0
    last_value = 0
    # check horizontal
    for i in range(board.len):
        count = 0
        for j in range(board.len):
            if board[i][j] == last_value: count += 1
            else:
                last_value = board[i][j]
                count = 0
            if last_value != 0 and count == 4: return last_value
    # check vertical
    for i in range(board.len):
        count = 0
        for j in range(board.len):
            if board[j][i] == last_value: count += 1
            else:
                last_value = board[j][i]
                count = 0
            if last_value != 0 and count == 4: return last_value
    # check diagonal right
    # first half of board
    for i in range(board.len):
        for b in range(i):
            if board[i-b,b] == last_value: count += 1
            else:
                last_value = board[i-b,b]
                count = 0
            if last_value != 0 and count == 4: return last_value
    # second half of board
    
    # check diagonal left
        # switch i and b from above
    # no win
    return None

def minimax(board, row, col, move_num, alpha, beta):
    #if has_winner(): return None
    # minumum moves to win is 7
    if move_num < 7: return None

# for our example -- hopefully will cluster near the middle
def example_pick_move(board):
    row = 3
    col = 3
    while (True):
        if board[row][col] == 0:
            print(row, col)
            return {"row": row, "col": col}
        else:
            row = (row + randint(-1,1)) % 7
            col = (col + randint(-1,1)) % 7

# check 3-in-a-row to avoid running minimax in win-now situations
def hasPartialWin(board, x):
    def check_direction(row, col, direction):
        s = ""
        end_row = row + 3*direction[0]
        end_col = col + 3*direction[1]
        if end_row < 0 or end_row >= len(board) or end_col < 0 or end_col >= len(board[0]):
            return False
        for i in [0, 1, 2, 3]:
            s += str(board[row+i*direction[0]][col+i*direction[1]])
        # print(s)
        if s == f"0{x}{x}{x}":
            return row, col
        if s == f"{x}0{x}{x}":
            return row + direction[0], col + direction[1]
        if s == f"{x}{x}0{x}":
            return row + 2*direction[0], col + 2*direction[1]
        if s == f"{x}{x}{x}0":
            return row + 3*direction[0], col + 3*direction[1]
        return False
    for i in range(len(board)):
        for j in range(len(board[0])):
            # Check horizontal
            result = check_direction(i, j, (0, 1))
            if result:
                return result
            # Check vertical
            result = check_direction(i, j, (1, 0))
            if result:
                return result
            # Check diagonal (top-left to bottom-right)
            result = check_direction(i, j, (1, 1))
            if result:
                return result
            # Check diagonal (top-right to bottom-left)
            result = check_direction(i, j, (1, -1))
            if result:
                return result
    return False

def next_move(board, move):
    # the input is in the form of a 9x9 matrix with the following values
    # 0 represents open squares
    # 1 represents squares already occupied by the bot
    # -1 represents squares already occupied by the user
    print(*board, sep="\n")
    # quick out for win-now situations
    botWin = hasPartialWin(board, 1)
    if botWin:
        print("bot win")
        return {"row": botWin[0], "col": botWin[1]}
    userWin = hasPartialWin(board, -1)
    if userWin:
        print("blocking user win")
        return {"row": userWin[0], "col": userWin[1]}
    #TODO: IMPLEMENT AI STUFF HERE
    bot = TicTacToe2(board)
    return bot.find_best_move()
    # Keep the return value of the function in this format
    # return example_pick_move(board)
