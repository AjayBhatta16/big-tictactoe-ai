import threading
import concurrent.futures
import random

class TicTacToe2:
    PLAYER_X = -1
    PLAYER_O = 1
    EMPTY = 0
    SIZE = 7
    MAX_DEPTH = 2

    def __init__(self, board):
        self.board = board

    def check_win(self):
        # Simplified checkWin for brevity; this will only check rows
        for i in range(self.SIZE):
            count_x = count_o = 0
            for j in range(self.SIZE):
                if self.board[i][j] == self.PLAYER_X:
                    count_x += 1
                    count_o = 0
                elif self.board[i][j] == self.PLAYER_O:
                    count_o += 1
                    count_x = 0
                else:
                    count_x = count_o = 0
                if count_x == 4 or count_o == 4:
                    return True
        return False

    def check_draw(self):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.board[i][j] == self.EMPTY:
                    return False
        return True

    

    def best_move(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_ai = executor.submit(self.find_best_move)
            future_spinner = executor.submit(self.display_spinner)

            try:
                future_ai.result()  # Wait for AI to finish computation
                future_spinner.cancel()  # Stop spinner once AI completes
            except Exception as e:
                print(e)

    def find_best_move(self):
        best_score = float('-inf')
        best_move_x = best_move_y = -1

        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.board[i][j] == self.EMPTY:
                    self.board[i][j] = self.PLAYER_O
                    move_score = self.minimax(0, False, float('-inf'), float('inf'))
                    self.board[i][j] = self.EMPTY
                    if move_score > best_score:
                        best_score = move_score
                        best_move_x, best_move_y = i, j

        return {"row": best_move_x, "col": best_move_y}

    def minimax(self, depth, is_max, alpha, beta):
        if self.check_win():
            return -10 if is_max else 10
        if self.check_draw() or depth == self.MAX_DEPTH:
            return self.heuristic_evaluation()

        if is_max:
            max_eval = float('-inf')
            for i in range(self.SIZE):
                for j in range(self.SIZE):
                    if self.board[i][j] == self.EMPTY:
                        self.board[i][j] = self.PLAYER_O
                        eval = self.minimax(depth + 1, False, alpha, beta)
                        self.board[i][j] = self.EMPTY
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(self.SIZE):
                for j in range(self.SIZE):
                    if self.board[i][j] == self.EMPTY:
                        self.board[i][j] = self.PLAYER_X
                        eval = self.minimax(depth + 1, True, alpha, beta)
                        self.board[i][j] = self.EMPTY
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def heuristic_evaluation(self):
        # Placeholder method; returns random value for simplicity
        return random.randint(-5, 5)
