#Board: This class represents an entire Sudoku board. A Board object has 81 Cell objects.

import pygame
from cell import Cell
from sudoku_generator import generate_sudoku

class Board:
    def __init__(self, width, height, screen, difficulty):

        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty

        # number of removed cells depends on difficulty
        if difficulty == "easy":
            removed = 30
        elif difficulty == "medium":
            removed = 40
        else:
            removed = 50

        # make sudoku puzzle
        self.board = generate_sudoku(9, removed)
        self.original = [row[:] for row in self.board]  # saved copy for reset

        # prepare cell objects
        self.cells = []
        self.selected = None
        self.cell_size = width // 9

        # create 81 cells
        for i in range(9):
            row_cells = []
            for k in range(9):
                value = self.board[i][k]
                cell = Cell(value, i, k, screen)
                row_cells.append(cell)
            self.cells.append(row_cells)

    # draw grid and all cells
    def draw(self):
        color = (0, 0, 0)  # black

        # draw horizontal and vertical lines
        for i in range(10):
            # thick line every 3 rows/columns
            if i % 3 == 0:
                line_thickness = 4
            else:
                line_thickness = 1

            # horizontal line
            pygame.draw.line(
                self.screen,
                color,
                (0, i * self.cell_size),
                (self.width, i * self.cell_size),
                line_thickness)

            # vertical line
            pygame.draw.line(
                self.screen,
                color,
                (i * self.cell_size, 0),
                (i * self.cell_size, self.height),
                line_thickness)

        # draw each cell
        for row in self.cells:
            for cell in row:
                cell.draw()


    # select a cell by row and column
    def select(self, i, k):
        # unselect previous cell
        if self.selected is not None:
            old_i, old_k = self.selected
            self.cells[old_i][old_k].selected = False

        # select new one
        self.cells[i][k].selected = True
        self.selected = (i, k)


    # convert mouse click (x,y) into (row,col)
    def click(self, x, y):
        # if click outside board
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None

        i = y // self.cell_size
        k = x // self.cell_size
        return (i, k)


    # clear selected cell (only if editable)
    def clear(self):
        if self.selected is None:
            return

        i, k = self.selected

        # only erase user cells (original puzzle numbers can't be changed)
        if self.original[i][k] == 0:
            self.cells[i][k].set_cell_value(0)
            self.cells[i][k].set_sketched_value(0)


    # sketch (write small number in corner)
    def sketch(self, value):
        if self.selected is None:
            return

        i, k = self.selected

        if self.original[i][k] == 0:
            self.cells[i][k].set_sketched_value(value)


    # place final number into selected cell
    def place_number(self, value):
        if self.selected is None:
            return

        i, k = self.selected

        if self.original[i][k] == 0:
            self.cells[i][k].set_cell_value(value)
            self.cells[i][k].set_sketched_value(0)
            self.update_board()


    # reset puzzle to original state
    def reset_to_original(self):
        for i in range(9):
            for k in range(9):
                original_value = self.original[i][k]
                self.cells[i][k].set_cell_value(original_value)
                self.cells[i][k].set_sketched_value(0)

        self.update_board()


    # true if no empty cells left
    def is_full(self):
        for i in range(9):
            for k in range(9):
                if self.cells[i][k].value == 0:
                    return False
        return True


    # copy values from Cell objects back to board list
    def update_board(self):
        for i in range(9):
            for k in range(9):
                self.board[i][k] = self.cells[i][k].value


    # find the first empty cell
    def find_empty(self):
        for i in range(9):
            for k in range(9):
                if self.cells[i][k].value == 0:
                    return (i, k)
        return None


    # check if solved correctly
    def check_board(self):
        # check rows
        for i in range(9):
            used = set()
            for k in range(9):
                v = self.cells[i][k].value
                if v < 1 or v > 9 or v in used:
                    return False
                used.add(v)

       
