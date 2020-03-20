import pygame
from pygame.locals import *

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

class Grid:
    # Grid is a square grid of Square objects (9x9 in sudoku)
    
    grid_values = [
        [3,0,6,5,0,8,4,0,0],
        [5,2,0,0,0,0,0,0,0],
        [0,8,7,0,0,0,0,3,1],
        [0,0,3,0,1,0,0,8,0],
        [9,0,0,8,6,3,0,0,5],
        [0,5,0,0,9,0,6,0,0],
        [1,3,0,0,0,0,2,5,0],
        [0,0,0,0,0,0,0,7,4],
        [0,0,5,2,0,6,3,0,0]
    ]
    
    # args of __init__ (except self) are args of object on instantiation
    def __init__(self, grid_size, square_width):
        self._running = True # loop continues while _running is True
        self._display_surf = None
        self.square_width = square_width
        self.grid_size = grid_size
        self.model = None
        self.window_dims = (grid_size*square_width, grid_size*square_width)
        self.puzzle_grid = [[Square(self.grid_values[row][col], row, col,
                            square_width) for col in range(grid_size)] 
                                            for row in range(grid_size)]
        self.update_model()

    def update_model(self):
        self.model = [[self.puzzle_grid[row][col].value 
                             for col in range(self.grid_size)] 
                             for row in range(self.grid_size)]

    def draw(self):
        gap = self.square_width
        # draw grid lines - want lines at beginning AND end (+1)
        for i in range(self.grid_size+1):
            line_width = 4 if (i%3==0 and i!=0) else 1
            start_pos = (0, i*gap) # top row
            end_pos = (9*gap, i*gap) # bottom row
            pygame.draw.line(self._display_surf, (0, 0, 0), start_pos,
                             end_pos, line_width)
            start_pos = (i*gap, 0) # top row
            end_pos = (i*gap, 9*gap) # bottom row
            pygame.draw.line(self._display_surf, (0, 0, 0), start_pos,
                             end_pos, line_width)
        # Draw squares (number and outline)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.puzzle_grid[i][j].draw_square(self._display_surf)
        pygame.display.update() # makes changes visible

    def on_init(self):
        pygame.font.init()
        pygame.init() # initializes all pygame modules
        self._display_surf = pygame.display.set_mode(self.window_dims)
        self._display_surf.fill((255,255,255))
        self.draw()
        self._running = True

    def on_event(self, event):
        # check for quit - setting _running to False breaks game loop
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.solve_puzzle()
                print("space song")

    def on_cleanup(self):
        pygame.quit() # quits all pygame modules

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event) # get key/other inputs
        self.on_cleanup()

    def solve_puzzle(self):
        zero_coords = find_zero(self.model)
        if not(zero_coords):
            return True # if no zeros on board
        else:
            row, col = zero_coords
        for candidate in range(1,10):
            if possible(self.model, candidate, row, col):
                self.model[row][col] = candidate
                self.puzzle_grid[row][col].set(candidate)
                self.puzzle_grid[row][col].draw_coloured(self._display_surf, GREEN)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(10)

                if self.solve_puzzle():
                    return True

                self.model[row][col] = 0
                self.puzzle_grid[row][col].set(0)
                self.update_model()
                self.puzzle_grid[row][col].draw_coloured(self._display_surf, RED)
                pygame.display.update()
                pygame.time.delay(10)
        return False

class Square:
    N = 9 # for NxN puzzle
    def __init__(self, value, row, col, width):
        self.value = value # value (0-9) of square
        self.row = row # row in grid
        self.col = col # column in grid
        self.width = width # dimension of square is width-by-width
        self.selected = False # highligh square when targeted

    def draw_square(self, display):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width
        x = self.row*gap
        y = self.col*gap
        if self.value != 0:
            # render: params text, antialias(T/F?), color
            text = fnt.render(str(self.value), 1, BLACK)
            display.blit(text, (x + (gap/2 - text.get_width()/2),
                                      y + (gap/2-text.get_height()/2)))

    def draw_coloured(self, display, colour):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width
        x = self.row*gap
        y = self.col*gap
        
        pygame.draw.rect(display, WHITE, (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        display.blit(text, (x + (gap/2 - text.get_width()/2), 
                        y + (gap/2 - text.get_height()/2)))
        pygame.draw.rect(display, colour, (x, y, gap, gap), 3)

    def set(self, val):
        # sets value in square
        self.value = val

def find_zero(model):
    # find position of first 0 (left to right, top-down) in "model" matrix
    for row in range(len(model)):
        for col in range(len(model[0])):
            if model[row][col]==0:
                return (row, col) # position of first 0
    return None # if no 0s on board

def possible(model, candidate, row, col):
    #check 3x3 grid
    for i in range(row-row%3, row-row%3+3):
        for j in range(col-col%3, col-col%3+3):
            if candidate==model[i][j]:
                return False
    #check row
    for j in range(9):
        if candidate==model[row][j]:
                return False
    #check column
    for i in range(9):
        if candidate==model[i][col]:
                return False
    return True

if __name__ == "__main__":
    my_grid = Grid(9, 50) # 9x9 puzzle, square width 50 (board size 450x450)
    my_grid.on_execute()