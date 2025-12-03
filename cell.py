#Cell: This class represents a single cell in the Sudoku board. There are 81 Cells in a Board.
import pygame

class Cell:
    #Constructor for the Cell class
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0
        self.selected = False

    #Setter for this cell’s value
    def set_cell_value(self, value):
        self.value = value

    #Setter for this cell’s sketched value
    def set_sketched_value(self, value):
        self.sketched_value = value

    #Draws this cell, along with the value inside it.
    #If this cell has a nonzero value, that value is displayed.
    #Otherwise, no value is displayed in the cell.
    #The cell is outlined red if it is currently selected.
    def draw(self):
        cell_size = 60
        x = self.col * cell_size
        y = self.row * cell_size

        #outline colors
        red = (255, 0, 0)
        black = (0, 0, 0)

        if self.selected:
            thickness = 3
            outline_color = red
        else:
            thickness = 1
            outline_color = black

        pygame.draw.rect(self.screen, outline_color,(x, y, cell_size, cell_size), thickness)

        #font colors
        light_gray = (150, 150, 150)
        dark_blue = (30, 50, 100)

        if self.value != 0: #draws real value (bigger font)
            font = pygame.font.Font(None, 40)
            #different colors if given or user input
            if self.given:
                color = dark_blue
            else:
                color = black

            text = font.render(str(self.value), True, color)
            self.screen.blit(text, (x + 22, y + 18))

        elif self.value == 0 and self.sketched_value != 0: #draws sketched value (smaller font)
            font = pygame.font.Font(None, 25)
            text = font.render(str(self.sketched_value), True, light_gray)
            self.screen.blit(text, (x + 5, y + 5))