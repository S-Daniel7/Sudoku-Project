
import pygame
import sys
from board import Board

pygame.init()

# window size
WIDTH = 540
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game!")

# colors
WHITE = (255, 255, 255)
GRAY  = (200, 200, 200)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# draw a rectangular button

def draw_button(text, x, y, w, h):
    pygame.draw.rect(SCREEN, GRAY, (x, y, w, h))
    font = pygame.font.Font(None, 46)
    label = font.render(text, True, BLACK)
    SCREEN.blit(label, (x + w//2 - label.get_width()//2,
                        y + h//2 - label.get_height()//2))
    return pygame.Rect(x, y, w, h)

# start screen

def start_screen():
    SCREEN.fill(WHITE)

    # title
    font = pygame.font.Font(None, 80)
    title = font.render("Sudoku Game", True, BLACK)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 90))

    # buttons
    easy_btn = draw_button("Easy",   170, 200, 200, 50)
    med_btn = draw_button("Medium", 170, 280, 200, 50)
    hard_btn = draw_button("Hard",   170, 360, 200, 50)

    pygame.display.update()

    # wait for a click
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if easy_btn.collidepoint(x, y):
                    return "easy"
                if med_btn.collidepoint(x, y):
                    return "medium"
                if hard_btn.collidepoint(x, y):
                    return "hard"



# win or lose screen

def end_screen(win):
    SCREEN.fill(WHITE)

    font = pygame.font.Font(None, 60)

    if win:
        msg = font.render("Yay! You Win!", True, BLUE)
    else:
        msg = font.render("Game Over :(", True, RED)

    SCREEN.blit(msg, (WIDTH//2 - msg.get_width()//2, 200))

    restart_btn = draw_button("Restart", 170, 350, 200, 60)
    exit_btn    = draw_button("Exit",    170, 430, 200, 60)

    pygame.display.update()

    # wait for click
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if restart_btn.collidepoint(x, y):
                    return "restart"
                if exit_btn.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()


# main game

def play_game(difficulty):
    board = Board(540, 540, SCREEN, difficulty)

    while True:
        SCREEN.fill(WHITE)
        board.draw()

        reset_btn   = draw_button("Reset",   20, 550, 150, 40)
        restart_btn = draw_button("Restart", 195, 550, 150, 40)
        exit_btn    = draw_button("Exit",    370, 550, 150, 40)

        pygame.display.update()

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                # click buttons
                if reset_btn.collidepoint(x, y):
                    board.reset_to_original()

                if restart_btn.collidepoint(x, y):
                    return "restart"

                if exit_btn.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

                # inside board
                if y < 540:
                    cell_pos = board.click(x, y)
                    if cell_pos:
                        i, k = cell_pos
                        board.select(i, k)


            if event.type == pygame.KEYDOWN:

                # backspace clear
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    board.clear()

                # numbers 1–9 to place or sketch
                if pygame.K_1 <= event.key <= pygame.K_9:
                    value = event.key - pygame.K_0

                    # shift = sketch 
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        board.sketch(value)
                    else:
                        board.place_number(value)

                # submitting sketched number
                if event.key == pygame.K_RETURN:
                    if board.selected:
                        i, k = board.selected
                        if board.cells[i][k].sketched_value != 0:
                            board.place_number(board.cells[i][k].sketched_value)

        # to check if the puzzle is finished, return win or lose
        if board.is_full():
            correct = board.check_board()
            return "win" if correct else "lose"


# main program loop

def main():
    while True:
        difficulty = start_screen()
        result = play_game(difficulty)

        if result == "restart":
            continue

        if result == "win":
            choice = end_screen(True)
            if choice == "restart":
                continue

        if result == "lose":
            choice = end_screen(False)
            if choice == "restart":
                continue


if __name__ == "__main__":
    main()

