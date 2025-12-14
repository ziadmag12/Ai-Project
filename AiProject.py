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
