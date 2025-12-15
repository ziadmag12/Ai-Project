import tkinter as tk
from tkinter import messagebox
import math
import random
from copy import deepcopy

ROWS = 6
COLUMNS = 7
CONNECT_N =  4 

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2


CELL_SIZE = 80
PADDING = 5

SCORE_FOUR = 100000       
SCORE_THREE = 50          
SCORE_TWO = 5             
SCORE_BLOCKED_THREE = 20  
CENTER_WEIGHT = 4       

INF = math.inf 

class Board:
    def __init__(self):
        self.board = [[EMPTY for col in range(COLUMNS)] for row in range(ROWS)]

    def clone(self):
        new_board = Board()
        new_board.board = deepcopy(self.board)
        return new_board

    def drop_piece(self, col, piece):
        for row in range(ROWS - 1, -1, -1): 
            if self.board[row][col] == EMPTY:
                self.board[row][col] = piece
                return row
        return None

    def remove_piece(self, col):
        for r in range(ROWS):
            if self.board[r][col] != EMPTY:
                self.board[r][col] = EMPTY
                return True
        return False

    def get_valid_locations(self):
        return [col for col in range(COLUMNS) if self.board[0][col] == EMPTY]

    def is_full(self):
        return not self.get_valid_locations()


def check_horizontal(board_data, piece):
    for r in range(ROWS):
        for c in range(COLUMNS - CONNECT_N + 1):
            if board_data[r][c:c + CONNECT_N].count(piece) == CONNECT_N:
                return True
    return False


def check_vertical(board_data, piece):
    for c in range(COLUMNS):
        for r in range(ROWS - CONNECT_N + 1):
            window = [board_data[r + i][c] for i in range(CONNECT_N)]
            if window.count(piece) == CONNECT_N:
                return True
    return False


def check_diagonal_up(board_data, piece):
    for r in range(CONNECT_N - 1, ROWS):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = [board_data[r - i][c + i] for i in range(CONNECT_N)]
            if window.count(piece) == CONNECT_N:
                return True
    return False


def check_diagonal_down(board_data, piece):
    for r in range(ROWS - CONNECT_N + 1):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = [board_data[r + i][c + i] for i in range(CONNECT_N)]
            if window.count(piece) == CONNECT_N:
                return True
    return False


def check_win(board_instance, piece):
    board_data = board_instance.board
    return (
        check_horizontal(board_data, piece) or
        check_vertical(board_data, piece) or
        check_diagonal_up(board_data, piece) or
        check_diagonal_down(board_data, piece)
    )


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    count_piece = window.count(piece)
    count_opp = window.count(opp_piece)
    count_empty = window.count(EMPTY)

    if count_piece == 4:
        score += SCORE_FOUR
    elif count_piece == 3 and count_empty == 1:
        score += SCORE_THREE
    elif count_piece == 2 and count_empty == 2:
        score += SCORE_TWO

    if count_opp == 3 and count_empty == 1:
        score -= SCORE_BLOCKED_THREE

    return score



# Heuristic evaluation functions for AI (position scoring)
def get_position_score(board_instance, piece):
    board_data = board_instance.board
    score = 0
    center_col = COLUMNS // 2

    center_count = sum(1 for r in range(ROWS) if board_data[r][center_col] == piece)
    score += center_count * CENTER_WEIGHT
    
    for r in range(ROWS):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = board_data[r][c:c + CONNECT_N]
            score += evaluate_window(window, piece)

    for c in range(COLUMNS):
        for r in range(ROWS - CONNECT_N + 1):
            window = [board_data[r + i][c] for i in range(CONNECT_N)]
            score += evaluate_window(window, piece)
            
    for r in range(CONNECT_N - 1, ROWS):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = [board_data[r - i][c + i] for i in range(CONNECT_N)]
            score += evaluate_window(window, piece)

    for r in range(ROWS - CONNECT_N + 1):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = [board_data[r + i][c + i] for i in range(CONNECT_N)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return (
        check_win(board, PLAYER_PIECE)
        or check_win(board, AI_PIECE)
        or board.is_full()
    )


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = board.get_valid_locations()

    if depth == 0 or is_terminal_node(board):
        if check_win(board, AI_PIECE):
            return None, SCORE_FOUR
        elif check_win(board, PLAYER_PIECE):
            return None, -SCORE_FOUR
        else: 
            return None, get_position_score(board, AI_PIECE)

   
    best_col = random.choice(valid_locations) if valid_locations else None

    if maximizingPlayer:
        value = -INF
        for col in valid_locations:
            board.drop_piece(col, AI_PIECE)
            _, score = minimax(board, depth - 1, alpha, beta, False)
            board.remove_piece(col)

            if score > value:
                value = score
                best_col = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    else: 
        value = INF
        for col in valid_locations:
            board.drop_piece(col, PLAYER_PIECE)
            _, score = minimax(board, depth - 1, alpha, beta, True)
            board.remove_piece(col)

            if score < value:
                value = score
                best_col = col

            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

class MinimaxAgent:
    def __init__(self, depth=3):
        self.depth = depth

    def pick_best_move(self, board):
        col, _ = minimax(board, self.depth, -INF, INF, True)
        valid = board.get_valid_locations()
       
        return col if col in valid else random.choice(valid)








class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4 AI")

        self.board = Board()
        self.ai = MinimaxAgent(depth=3)
        self.turn = PLAYER_PIECE

        canvas_width = COLUMNS * CELL_SIZE
        canvas_height = ROWS * CELL_SIZE
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="blue")
        self.canvas.pack()

        self.draw_board()
        self.canvas.bind("<Button-1>", self.click_event)

        self.restart_button = tk.Button(root, text="Restart Game", command=self.restart_game)
        self.restart_button.pack(pady=10)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLUMNS):
                x1 = c * CELL_SIZE + PADDING
                y1 = r * CELL_SIZE + PADDING
                x2 = (c + 1) * CELL_SIZE - PADDING
                y2 = (r + 1) * CELL_SIZE - PADDING
                piece = self.board.board[r][c]
                color = "white"
                if piece == PLAYER_PIECE:
                    color = "red"
                elif piece == AI_PIECE:
                    color = "yellow"
                self.canvas.create_oval(x1, y1, x2, y2, fill=color)

    def click_event(self, event):
        col = event.x // CELL_SIZE
        
        if col < 0 or col >= COLUMNS or self.turn != PLAYER_PIECE or self.board.board[0][col] != EMPTY:
            return

        self.board.drop_piece(col, PLAYER_PIECE)
        self.draw_board()

        if check_win(self.board, PLAYER_PIECE):
            messagebox.showinfo("Game Over", "You win! 🎉")
            self.turn = EMPTY
            return

        if self.board.is_full():
            messagebox.showinfo("Game Over", "Draw!")
            self.turn = EMPTY
            return

        self.turn = AI_PIECE
        self.root.after(200, self.ai_move) 
    def ai_move(self):
        if self.turn != AI_PIECE: return

        col = self.ai.pick_best_move(self.board)

        self.board.drop_piece(col, AI_PIECE)
        self.draw_board()

        if check_win(self.board, AI_PIECE):
            messagebox.showinfo("Game Over", "AI Wins! 💻")
            self.turn = EMPTY
            return

        if self.board.is_full():
            messagebox.showinfo("Game Over", "Draw!")
            self.turn = EMPTY
            return

        self.turn = PLAYER_PIECE

    def restart_game(self):
        self.board = Board()
        self.turn = PLAYER_PIECE
        self.draw_board()


if __name__ == "__main__":
    root = tk.Tk()
    Connect4GUI(root)
    root.mainloop()
