import sys
import copy
import pygame
import random
import numpy as np #For board

from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')

class Board:
    def __init__(self):
        self.squares = np.zeros((ROW, COL))  # Numpy array is filled with zeros
        self.empty_sqrs = self.squares.copy() #List of empty sqrs -> all srq at start
        self.marked_sqrs = 0 #Not list but a number
    
    def final_state(self,show=False):
        '''
        @ retuen 0 if there is no win yet ->does not mean draw
        @ return 1 if p1 wins
        @ return 2 if p2 wins
        '''
        #Vertical wins
        for col in range(COL):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] !=0:#check empty
                if show:
                    color = CIRC_COLOR if self.squares[0][col]==2 else CROSS_COLOR
                    ipos = (col*SQ_SIZE + SQ_SIZE//2,20)
                    fpos = (col*SQ_SIZE + SQ_SIZE//2,HEIGHT-20)
                    pygame.draw.line(screen,color,ipos,fpos,LINE_WIDTH)
                return self.squares[0][col] # @ return 1 if p1 wins
        #Horizontal wins
        for row in range(ROW):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] !=0:#check empty
                if show:
                    color = CIRC_COLOR if self.squares[row][0]==2 else CROSS_COLOR
                    ipos = (20,row*SQ_SIZE + SQ_SIZE//2)
                    fpos = (WIDTH-20,row*SQ_SIZE + SQ_SIZE//2)
                    pygame.draw.line(screen,color,ipos,fpos,LINE_WIDTH)
                return self.squares[row][0] # @ return 1 if p1 wins
            
        #desc diognel
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] !=0:
            if show:
                    color = CIRC_COLOR if self.squares[0][0]==2 else CROSS_COLOR
                    ipos = (20,20)
                    fpos = (WIDTH-20,HEIGHT-20)
                    pygame.draw.line(screen,color,ipos,fpos,LINE_WIDTH)
            return self.squares[1][1]
        #asc diognel
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] !=0:
            if show:
                    color = CIRC_COLOR if self.squares[2][0]==2 else CROSS_COLOR
                    ipos = (20,HEIGHT-20)
                    fpos = (WIDTH-20,20)
                    pygame.draw.line(screen,color,ipos,fpos,LINE_WIDTH)
            return self.squares[1][1]
        
        return 0 # No win yet

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1
        
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROW):
            for col in range(COL):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))
        return empty_sqrs
    
    def isfull(self):
        return self.marked_sqrs == 9
    
    def isempty (self):
        return self.marked_sqrs==0
    
class AI:
    #Level = 0 is random Ai
    #Level = 1 is miimax
    def __init__(self, level=1, player = 2):
        self.level = level
        self.player = player
    #Going to resive our selvesand a bord
    def eval(self,main_board):
        if self.level==0:
            #Random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            #minimax
            #AI is gonna minimize
            eval,move = self.minimax(main_board , False)
        print(f'AI chose pos {move} with eval {eval}')
        return move # row,col

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()  # Get a list of empty squares
        idx = random.randrange(0, len(empty_sqrs))  # Generate a random index within the range of available empty squares
        return empty_sqrs[idx]  # Return the randomly chosen empty square (row, col) tuple
    
    def minimax(self, board, maximizing):
        
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 2 # 1 - cross // 2 - circle
        self.gamemode = 'ai'
        self.running = True
        self.show_lines()

    def make_move(self,row,col):
        self.board.mark_sqr(row,col,self.player)#Mark sq
        self.draw_fig(row,col)
        self.next_turn()

    def show_lines(self):
        #Fill Background clour
        screen.fill(BG_COLOR)
        # VERTICAL LINES                         
        pygame.draw.line(screen, LINE_COLOR, (SQ_SIZE, 0), (SQ_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH-SQ_SIZE, 0), (WIDTH-SQ_SIZE, HEIGHT), LINE_WIDTH)
        # HORIZONTAL LINES
        pygame.draw.line(screen, LINE_COLOR, (0,SQ_SIZE), (WIDTH, SQ_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQ_SIZE), (WIDTH, HEIGHT-SQ_SIZE), LINE_WIDTH)
        #Update Display
        pygame.display.flip()  # Update the display

    def draw_fig(self,row,col):
        #No need of player parameter bec we have acess to via self
        if self.player == 1:
            #Decending Line
            start_dec = (col * SQ_SIZE + OFFSET,row * SQ_SIZE+ OFFSET)
            end_dec = (col * SQ_SIZE + SQ_SIZE - OFFSET,row * SQ_SIZE + SQ_SIZE - OFFSET)
            pygame.draw.line(screen,CROSS_COLOR,start_dec,end_dec,CROSS_WIDTH)
            #Acending Line
            start_ace = (col * SQ_SIZE + OFFSET,row * SQ_SIZE + SQ_SIZE - OFFSET)
            end_ace = (col * SQ_SIZE + SQ_SIZE - OFFSET,row * SQ_SIZE + OFFSET)
            pygame.draw.line(screen,CROSS_COLOR,start_ace,end_ace,CROSS_WIDTH)

        elif self.player == 2:
            #draw circle
            center = (col * SQ_SIZE + SQ_SIZE // 2,row * SQ_SIZE + SQ_SIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center , RADIUS, CIRC_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1
        # (1%2)+1=1+1=2
        # (2%2)+1=0+1=1

    def change_game_mode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'
    
    def isover(self):

        return self.board.final_state(show = True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__() #Restart all atrs to default
        
def main():
    # game object
    game = Game()
    board = game.board #variable to easily acess board
    ai = game.ai
    #Game main loop
    while True: 
    #Event -> press screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:

                 # g-gamemode
                if event.key == pygame.K_g:
                    game.change_game_mode()

                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                #pos -> position in pygame
                pos = event.pos
                # int -> to prevent float values
                row = int(pos[1]//SQ_SIZE)
                col = int(pos[0]//SQ_SIZE)

                if board.empty_sqr(row,col) and game.running :#If sq is empt
                    game.make_move(row,col)

        pygame.display.update()

        if game.isover():  
            pygame.display.update()
            game.running = False
            pygame.display.update()

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            #ai methods
            row , col = ai.eval(board)
            game.make_move(row,col)
 
        pygame.display.update()
                              
main() 