import copy
from utils import Log, Game, Agent
from random import random
from functools import partial 
import pygame 
import os, sys 
from pygame.locals import * 
import threading, time, logging

# TODO - modify for n in a row, and for 3D
def checkGameOver(board, logger, dimension): 
    board = board[0]
    for i in range(3):
        inARow_V = True
        inARow_H = True
        startingPiece_H = board[i][0]
        startingPiece_V = board[0][i]
        for j in range(1, 3):
            if inARow_H and board[i][j] != startingPiece_H:
                inARow_H = False
            if inARow_V and board[j][i] != startingPiece_V:
                inARow_V = False
                break 
            
        if inARow_V and startingPiece_V != 0:
            logger.d(f"Vertical: {i}")
            return True, startingPiece_V

        if inARow_H and startingPiece_H != 0:
            logger.d(f"Horizontal: {i}")
            return True, startingPiece_H
    
    diagOne = True
    diagTwo = True
    diagOneStarting = board[0][0]
    diagTwoStarting = board[2][2]
    for i in range(1, 3):
        if diagOne and board[i][i] != diagOneStarting:
            diagOne = False
        if diagTwo and board[2-i][2-i] != diagTwoStarting:
            diagTwo = False

    if diagOne and diagOneStarting!= 0: 
        logger.d(f"Diag One")
        return True
    
    if diagTwo and diagTwoStarting!= 0: 
        logger.d(f"Diag Two")
        return True

    return False


class TicTacToe(Game): 
    def __init__(self, agentOne, agentTwo, logger, config): 
        super().__init__(agentOne, agentTwo, logger, config.turnChooser) 

        self.threeDims = config.threeDims
        self.dim = config.dimension 
        self._init_state =  [[0]*self.dim for _ in range(self.dim)]
        self.reset_board()
        # self.board[0] is the first layer, self.board[1] is the second layer, and 
        # self.board[2] is the third layer 
        self.gameOverChecker = config.gameOverChecker
        self._max_turn = self.dim ** 2 
        self.config = config
    
    def display(self): 
        def display_procedure():
            WIDTH = 500 
            HEIGHT = 500
            MARGIN = 5 

            TILE_WIDTH = WIDTH / self.dim
            TILE_HEIGHT = HEIGHT / self.dim

            HEIGHT += (self.dim + 1) * MARGIN
            WIDTH += (self.dim + 1) * MARGIN

            pygame.init()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption(self.config.title)
            # pygame.mouse.set_visible(0)

            clock = pygame.time.Clock() 
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos() 
                        column = pos[0] // (TILE_WIDTH + MARGIN)
                        row = pos[1] // (TILE_HEIGHT + MARGIN) 
                        print("Click", pos, "Grid Coords: ", row, column)

                screen.fill((0, 0, 0))

                for i in range(len(self.board[0])):
                    for j in range(len(self.board[0][i])):
                        color = (255, 255, 255) 
                        if self.board[0][i][j] == 1:
                            color = (0, 255, 0)
                        elif self.board[0][i][j] == 2: 
                            color = (255, 0, 0)

                        pos = [(TILE_WIDTH + MARGIN) * j + MARGIN,
                               (TILE_HEIGHT + MARGIN) * i + MARGIN,
                               TILE_WIDTH,
                               TILE_HEIGHT]
                        pygame.draw.rect(screen,
                                         color,
                                         pos)


                clock.tick(60) # Make sure our game doesn't run faster than 60fps 
                pygame.display.flip() # Update the display.

        x = threading.Thread(target=display_procedure)
        x.start() 
        
        

    def reset_board(self): 
        if self.threeDims:
            self.board = [copy.deepcopy(self._init_state) for _ in range(self.dim)]
        else: 
            self.board = [copy.deepcopy(self._init_state)]

    def __str__(self):
        if self.threeDims: 
            s = ""
            for layer in range(self.dim): 
                s += f"Layer {layer} \n"
                s += "".join([" ".join(str(y) for y in x) + "\n" for x in self.board[layer]])
            return s 
        else: 
            return "".join([" ".join(str(y) for y in x) + "\n" for x in self.board[0]])

    def makeMove(self, action):
        # TODO: update for 3 dims 
        # Assumes the move is valid
        pieceToPlay = 1 if self.currPlayer == 0 else 2
        self.board[0][action[0]][action[1]] = pieceToPlay
        return True

    def checkGameOver(self):
        return self.gameOverChecker(self.board, self.logger)

class ValueAgent(Agent):
    def __init__(self, playerNum, valueFunction): 
        super().__init__(playerNum)

        self.valueFunction = valueFunction
    
    def getMove(self, board): 
        action = self.valueFunction(board)
        return self.convert(action) 

    def convert(self, action):
        return (action % self.dim, action // self.dim)

class DumbAgent(Agent): 
    # TODO: update for 3 dims 
    def getMove(self, board): 
        dim = len(board[0])
        board = board[0]
        for i in range(dim):
            for j in range(dim):
                if board[i][j] == 0:
                    return (i, j)

threeInARow = partial(checkGameOver, dimension=3)
fourInARow = partial(checkGameOver, dimension=4)
fiveInARow = partial(checkGameOver, dimension=5)

def defaultTurnChooser(currPlayer):
    '''
    The default turn chooser just alternates between player 0 and player 1.  
    '''
    if currPlayer == 0: 
        return 1
    else: 
        return 0 

def randomTurnChooser(currPlayer): 
    return round(random()) 

def StandardTicTacToe(agentOne, agentTwo, log):
    config = TicTacToeConfig(turnChooser=defaultTurnChooser, gameOverChecker=threeInARow, dimension=3, threeDims=False)
    return TicTacToe(agentOne, agentTwo, log, config)

def InverseTicTacToe(agentOne, agentTwo, log): 
    # Inverse the result in the case of wins 
    def gameCheck(board, log): 
        res = threeInARow(board, log) 
        if res == 1: 
            return 2
        elif res == 2: 
            return 1

        return 0

    config = TicTacToeConfig(turnChooser=defaultTurnChooser, gameOverChecker=gameCheck, dimension=3, threeDims=False)
    return TicTacToe(agentOne, agentTwo, log, config)

def RandomTurnTicTacToe(agentOne, agentTwo, log): 
    config = TicTacToeConfig(turnChooser=randomTurnChooser, gameOverChecker=threeInARow, dimension=3, threeDims=False)
    return TicTacToe(agentOne, agentTwo, log, config)

def FourByFourTicTacToe(agentOne, agentTwo, log):
    config = TicTacToeConfig(turnChooser=defaultTurnChooser, gameOverChecker=fourInARow, dimension=4, threeDims=False)
    return TicTacToe(agentOne, agentTwo, log, config)

def FiveByFiveTicTacToe(agentOne, agentTwo, log): 
    config = TicTacToeConfig(turnChooser=defaultTurnChooser, gameOverChecker=fiveInARow, dimension=5, threeDims=False)
    return TicTacToe(agentOne, agentTwo, log, config)

def BigTicTacToe(agentOne, agentTwo, log): 
    config = TicTacToeConfig(turnChooser=defaultTurnChooser, gameOverChecker=fourInARow, dimension=4, threeDims=True)
    return TicTacToe(agentOne, agentTwo, log, config)

class TicTacToeConfig: 
    def __init__(self, gameOverChecker = threeInARow, turnChooser = defaultTurnChooser, dimension = 3, threeDims = False):
        self.gameOverChecker = gameOverChecker
        self.turnChooser = turnChooser 
        self.dimension = dimension
        self.threeDims = threeDims
        self.title = "TicTacToe"

if __name__ == "__main__":
    game = BigTicTacToe(DumbAgent(0), DumbAgent(1), Log(0))
    game.display()
    time.sleep(2)
    game.play()
    game.reset()
    game.play()
