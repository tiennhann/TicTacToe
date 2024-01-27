import sys      # Help us to quit the application
import pygame
import numpy as np

from constant import *

# PYGAME set up
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(background_color)

class Board:
    def __init__(self):
        self.squares = np.zeros((rows, columns))
        self.empty_squares = self.squares #list of empty squares.
        self.marked_squares = 0
    
    def final_state(self):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 win
            @return 2 if player 2 win
        '''
        # Vertical win
        for col in range(columns):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]

        # Horizontal win
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
        
        # descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
        
        # Ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]

        # No win yet
        return 0
    def mark_squares(self, row, col,player):
        self.squares[row][col] = player
        self.marked_squares +=1 # let us know if the board is full
    
    def empty_square(self,row, col):
        return self.squares[row][col] == 0
    
    def get_empty_squares(self):
        empty_squares = []
        for row in range (rows):
            for col in range (columns):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))
    
    def is_full (self):
        return self.marked_squares == 9
    
    def is_empty(self):
        return self.marked_squares == 0

class Game:
    # This method call each time we create new game object
    def __init__(self):
        self.board = Board()
        # self.ai = AI()
        self.player = 1 # which is the next player mark the square, 1 is cross (X), 2 is circle (O)
        self.gamemode = 'pvp' # pvp or ai
        self.running = True
        self.show_lines()

    def show_lines(self):
        # Vertical line: lines(surface, color, closed, points, width=1)
        pygame.draw.line(screen, line_color, (sq_size, 0), (sq_size,height), line_width)
        pygame.draw.line(screen, line_color, (width-sq_size, 0), (width-sq_size,height), line_width)

        # Horizontal line
        pygame.draw.line(screen, line_color, (0,sq_size), (height,sq_size), line_width)
        pygame.draw.line(screen, line_color, (0,width-sq_size), (height, width-sq_size), line_width)

    def next_turn(self):
        self.player = self.player % 2 + 1

    # This function draw line x or o for the game
    def draw_fig (self,row, col):
        if self.player == 1:
            #draw X
            # desc line
            start_desc = (col * sq_size + offset, row * sq_size + offset)
            end_desc = (col * sq_size + sq_size - offset, row * sq_size + sq_size - offset)
            pygame.draw.line(screen, cross_color, start_desc, end_desc, cross_width)

            # ascending line
            start_asc = (col * sq_size + offset, row * sq_size + sq_size- offset)
            end_asc = (col * sq_size + sq_size - offset, row * sq_size + offset)
            pygame.draw.line(screen, cross_color, start_asc, end_asc, cross_width)

        if self.player == 2:
            # draw O
            center=(col * sq_size + sq_size // 2, row * sq_size + sq_size // 2)
            pygame.draw.circle(screen, circle_color, center, radius, circle_width)

def main ():
    # Object: init will be called and show_line in init will aslo be called
    game = Game()
    board = game.board

    # Main loop
    while True:
        # For loop throught all the event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # Convert the cordinate from pixel to row & column,
                # so we can mark the board
                # y-axis divide sq_size
                row = pos[1] // sq_size
                # x-axis divide sq_size
                col = pos[0] // sq_size
                
                if board.empty_square(row, col):
                    board.mark_squares(row, col, game.player)
                    game.draw_fig(row,col)
                    game.next_turn()

        pygame.display.update()

main()