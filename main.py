import pygame
import sys
from cell import Cell


pygame.init()

SCREEN_MIN_SIZE = 750  # Can be made to autoadjust after % of ur screen
amount_of_cells = 16  # The amount of cells is equal in rows and columns, 16x16
bomb_chance = 0.25

CELL_SIZE = SCREEN_MIN_SIZE // amount_of_cells  # how large can each cell be?
READJUSTED_SIZE = CELL_SIZE * amount_of_cells
CELL_WIDTH = CELL_HEIGHT = CELL_SIZE

SCREEN_WIDTH, SCREEN_HEIGHT = READJUSTED_SIZE, READJUSTED_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
BLACK = (0,0,0)
#WHITE = (255,255,255)
#GREEN = (0,255,0)
#RED   = (255,0,0)
#GRAY  = (128,128,128)

pygame.display.set_caption("MineSweeper")

''' Create 2D-list 16x16 '''
cells = [[x for x in range(amount_of_cells)] for x in range(amount_of_cells)]


def create_cells():
    """This function is meant to initialy generate all the cells and create the boundaries"""
    for row in range(amount_of_cells):
        for col in range(amount_of_cells):
            cell = Cell(row, col,CELL_WIDTH, CELL_HEIGHT, bomb_chance)
            cells[row][col] = cell


def add_bomb_count():
    """This function add and count bombs around the cell"""
    for x in range(amount_of_cells):
            for y in range(amount_of_cells):
                if cells[x][y].bomb == False:
                    count_bombs = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if x + i >= 0 and x + i < amount_of_cells and y + j >= 0 and y + j < amount_of_cells:
                                if cells[x + i][y + j].bomb == True:
                                    count_bombs += 1
                    cells[x][y].neighbouring_bombs = count_bombs


def draw_cells():
    """In this function we want to draw each cell, i.e call upon each cells .draw() method!"""
    for row in cells:
        for cell in row:
            cell.draw(screen)


def draw():
    """This function handles all the drawings to the screen, such as drawing rectangles, objects etc"""
    draw_cells()


def event_handler(event):
    """This function handles all events in the program"""
    if event.type == pygame.QUIT:
        terminate_program()

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Vänsterklick
        pos = pygame.mouse.get_pos()
        x = pos[0] // CELL_SIZE
        y = pos[1] // CELL_SIZE

        cells[x][y].selected = True


def run_setup():
    """This function is meant to run all code that is neccesary to setup the app, happends only once"""
    create_cells()
    add_bomb_count()


def terminate_program():
    """Functionality to call on whenever you want to terminate the program"""
    pygame.quit()
    sys.exit()


def main():
    run_setup()

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            event_handler(event)

        draw()
        pygame.display.update()

    terminate_program()


if __name__ == "__main__":
    main()