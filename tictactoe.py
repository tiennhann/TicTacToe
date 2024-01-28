import sys      # Help us to quit the application
import pygame
import random
import copy
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
    
    def final_state(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 win
            @return 2 if player 2 win
        '''
        # Vertical win
        for col in range(columns):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = circle_color if self.squares[0][col] == 2 else cross_color
                    initial_pos = (col * sq_size + sq_size//2, 20)
                    final_pos = (col * sq_size +sq_size//2, height -20)
                    pygame.draw.line(screen, color, initial_pos, final_pos, line_width)
                return self.squares[0][col]

        # Horizontal win
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = circle_color if self.squares[row][0] == 2 else cross_color
                    initial_pos = (20, row * sq_size + sq_size//2)
                    final_pos = (width - 20, row * sq_size + sq_size//2)
                    pygame.draw.line(screen, color, initial_pos, final_pos, line_width)
                return self.squares[row][0]
        
        # descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = circle_color if self.squares[1][1] == 2 else cross_color
                initial_pos = (20,20)
                final_pos = (width - 20, height - 20)
                pygame.draw.line(screen, color, initial_pos, final_pos, cross_width)
            return self.squares[1][1]
        
        # Ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = circle_color if self.squares[1][1] == 2 else cross_color
                initial_pos = (20,height-20)
                final_pos = (width - 20, 20)
                pygame.draw.line(screen, color, initial_pos, final_pos, cross_width)
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
        
        return empty_squares
    
    def is_full (self):
        return self.marked_squares == 9
    
    def is_empty(self):
        return self.marked_squares == 0

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player
    
    def rnd(self, board):
        empty_squares = board.get_empty_squares()
        idx = random.randrange(0, len(empty_squares))

        return empty_squares[idx]   # Return random (row, col)
    
    def minimax(self, board,  maximizing):
        # Check our terminal case
        case = board.final_state()

        # Player 1 wins
        if case == 1:
            return 1, None  # eval, move
        
        # Player 2 wins
        if case == 2:
            return -1, None

        # Draw
        elif board.is_full():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row,col) in empty_squares:
                temp_board = copy.deepcopy(board) # Copy the board to test all cases
                temp_board.mark_squares(row,col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row,col)
            return max_eval, best_move    
        
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row,col) in empty_squares:
                temp_board = copy.deepcopy(board) # Copy the board to test all cases
                temp_board.mark_squares(row,col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row,col)
            return min_eval, best_move       


    def eval(self, main_board):
        if self.level == 0:
            # Random choice
            eval = 'random'
            move = self.rnd(main_board)
            
        else:
            # Minimax algo choice
            eval, move = self.minimax(main_board, False)
        print(f'AI has chosen to mark the square in pos {move} with an eval of {eval}' )
        return move

class Game:
    # This method call each time we create new game object
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 # which is the next player mark the square, 1 is cross (X), 2 is circle (O), change this to 2 if you want AI go first
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()
    
    def make_move(self, row, col):
        self.board.mark_squares(row, col, self.player)
        self.draw_fig(row,col)
        self.next_turn()

    def show_lines(self):
        # fill background color
        screen.fill(background_color)
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

    def change_gamemode(self):
        if self.gamemode == 'pvp':
            self.gamemode= 'ai'
        else:
            self.gamemode = 'pvp'
    
    def reset(self):
        self.__init__()

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()

def main ():
    # Object: init will be called and show_line in init will aslo be called
    game = Game()
    board = game.board
    ai = game.ai

    # Main loop
    while True:
        # For loop throught all the event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                    # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    # to restart the board and the ai ( we have new board and new ai)
                    board = game.board
                    ai = game.ai

                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # Convert the cordinate from pixel to row & column,
                # so we can mark the board
                # y-axis divide sq_size
                row = pos[1] // sq_size
                # x-axis divide sq_size
                col = pos[0] // sq_size
                
                if board.empty_square(row, col) and game.running:
                    game.make_move(row,col)

                    if game.isover():
                        game.running = False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            # update the screen
            pygame.display.update() 

            # AI methods
            row, col = ai.eval(board)
            game.make_move(row,col)

            if game.isover():
                game.running = False

        pygame.display.update()

main()