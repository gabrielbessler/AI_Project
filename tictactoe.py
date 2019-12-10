import copy
from utils import Log, Game, Agent, Node
from random import random
from functools import partial
import pygame
import os, sys
from pygame.locals import *
import threading, time, logging
import argparse
import numpy

def checkGameOver(board, logger, n):
    zdmin = len(board)
    dim = len(board[0])

    def isValid(pos):
        return (0 <= pos[0] < zdmin and 0 <= pos[1] < dim and 0 <= pos[2] < dim)

    # Iterate through all starting position
    for k in range(zdmin):
        for i in range(dim):
            for j in range(dim):
                current = board[k][i][j]
                if current == 0:
                    continue
                horiz = True
                vert = True
                depth = True
                diagOne = True
                diagTwo = True
                diagThree = True
                diagFour = True
                diagFive = True
                diagSix = True

                for z in range(1, n):
                    pos = (k, i, j+z)
                    if not isValid(pos) or board[pos[0]][pos[1]][pos[2]] != current:
                        horiz = False

                    pos = (k, i+z, j)
                    if not isValid(pos) or board[pos[0]][pos[1]][pos[2]] != current:
                        vert = False

                    pos = (k+z, i, j)
                    if not isValid(pos) or board[pos[0]][pos[1]][pos[2]] != current:
                        depth = False

                    pos = (k, i+n, j+n)
                    if not isValid(pos) or board[pos[0]][pos[1]][pos[2]] != current:
                        diagOne = False

                    pos = (k, i-n, j+n)
                    if not isValid(pos) or board[pos[0]][pos[1]][pos[2]] != current:
                        diagTwo = False

                    pos = (k + n, i + n, j)
                    if not isValid(pos) or board[pos[0]][pos[1]][pos[2]] != current:
                        diagThree = False

                    pos = (k + n, i - n, j)
                    if not isValid(pos) or board[pos[0]][pos[1]][pos[2]] != current:
                        diagFour = False

                    pos = (k + n, i + n, j + n)
                    if not isValid(pos) or board[pos[0]][pos[1]][pos[2]] != current:
                        diagFive = False

                    pos = (k + n, i - n, j + n)
                    if not isValid(pos) or board[pos[0]][pos[1]][pos[2]] != current:
                        diagSix = False

                if horiz or vert or depth or diagOne or diagTwo or diagThree or diagFour or diagFive or diagSix:
                    return current

    return 0

class TicTacToe(Game):
    def __init__(self, agentOne, agentTwo, logger, config):
        super().__init__(agentOne, agentTwo, logger, config.turnChooser)

        self.threeDims = config.threeDims
        self.dim = config.dimension
        self._init_state =  [[0]*self.dim for _ in range(self.dim)]
        self.reset_board()
        # The first layer is self.board[0], self.board[1] is the second layer, and
        # self.board[2] is the third layer.
        self.gameOverChecker = config.gameOverChecker
        self._max_turn = self.dim ** 2
        self.config = config

        if agentOne is not None:
            self.agentOne.gameInitialized(self)

        if agentTwo is not None:
            self.agentTwo.gameInitialized(self)

    def getAllActions(self, onlyNumActions = False):
        '''
        Gets all of the available actions as 3-tuples or 
        count the number of available actions
        given the current board state.
        '''
        if onlyNumActions:
            actions = 0
        else:
            actions = []

        zdim = len(self.board)
        dim = len(self.board[0])
        for k in range(zdim):
            for i in range(dim):
                for j in range(dim):
                    if self.board[k][i][j] == 0:
                        if onlyNumActions:
                            actions += 1
                        else:
                            actions.append((k, i ,j))
        return actions

    def display(self):
        '''
        Render the TicTacToe board using pygame.
        '''
        def display_procedure():
            WIDTH = 500
            HEIGHT = 500
            MARGIN = 5

            TILE_WIDTH = WIDTH // self.dim
            TILE_HEIGHT = HEIGHT // self.dim

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
                        pos = [(TILE_WIDTH + MARGIN) * j + MARGIN,
                               (TILE_HEIGHT + MARGIN) * i + MARGIN,
                               TILE_WIDTH,
                               TILE_HEIGHT]
                        color = (255, 255, 255)
                        pygame.draw.rect(screen, color, pos)

                        if self.board[0][i][j] == 1:
                            color = (255, 0, 0)
                            pos = [(TILE_WIDTH + MARGIN) * (j) + MARGIN,
                               (TILE_HEIGHT + MARGIN) * (i+.33) + MARGIN,
                               TILE_WIDTH,
                               TILE_HEIGHT//3]
                            pygame.draw.rect(screen, color, pos)
                            pos = [(TILE_WIDTH + MARGIN) * (j+.33) + MARGIN,
                               (TILE_HEIGHT + MARGIN) * (i) + MARGIN,
                               TILE_WIDTH//3,
                               TILE_HEIGHT]
                            pygame.draw.rect(screen, color, pos)
                        elif self.board[0][i][j] == 2:
                            color2 = (0, 0, 255)
                            pygame.draw.circle(screen,
                                            color2,
                                            (int((j+0.5)*(TILE_WIDTH+MARGIN)),
                                            int((i+0.5)*(TILE_HEIGHT+MARGIN))), TILE_HEIGHT//2 - MARGIN//2)
                            pygame.draw.circle(screen,
                                            color,
                                            (int((j+0.5)*(TILE_WIDTH+MARGIN)),
                                            int((i+0.5)*(TILE_HEIGHT+MARGIN))), TILE_HEIGHT//2 - MARGIN//2 - 4)
                            #                 TILE_HEIGHT)

                clock.tick(60) # Make sure our game doesn't run faster than 60fps
                pygame.display.flip() # Update the display.

        x = threading.Thread(target=display_procedure)
        x.start()

    def reset_board(self):
        '''
        Return the board to its initial state. 
        '''
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
        '''
        Takes a move as a 3-tuple and updates the board accordingly. 

        Note: This assumes the move is valid
        '''
        pieceToPlay = self.currPlayer + 1
        self.board[action[0]][action[1]][action[2]] = pieceToPlay
        return True

    def checkGameOver(self):
        return self.gameOverChecker(self.board, self.logger)

class ValueAgent(Agent):
    def __init__(self, playerNum, valueFunction, dim):
        super().__init__(playerNum)

        self.valueFunction = valueFunction
        self.dim = dim

    def getMove(self, board, game):
        return self.valueFunction(board, game)

class AlphaZeroAgent(Agent):
    '''
    t is a float controlling degree of exploration, temperature variable
    model is the nn for MCTS
    isExploratory is a boolean that controls whether competitive or exploratory play
    '''
    def __init__(self, playerNum, isExploratory, t, dim, mcts):
        super().__init__(playerNum)
        self.dim = dim
        self.t = t
        self.MCTS = mcts
        self.isExploratory = isExploratory

    def getMove(self, board, game):
        #creates a state (a Node)from the board and game
        state = Node(copy.deepcopy(board), copy.deepcopy(game.currPlayer))
        self.MCTS.set_root(state, game)
        self.MCTS.perform_iterations(1000)
        if not self.isExploratory:
            action_visits = self.MCTS.N[self.MCTS.root]
            max_action = list(action_visits.keys())[0]
            max_visits = action_visits[max_action]
            for action in action_visits:
                if action_visits[action] > max_visits:
                    max_action = action
                    max_vists = action_visits[max_action]
            return max_action

        else:
            d = self.MCTS.N[self.MCTS.root]
            actions = [val ** (1 / self.t) for val in d.values()]
            total = sum(actions)
            actions = [val / total for val in actions]
            i = numpy.random.choice(numpy.arange(len(actions)), p=actions)
            return list(d.keys())[i]

class DumbAgent(Agent):
    def getMove(self, board, game):
        dim = len(board[0])
        zdim = len(board)
        for k in range(zdim):
            for i in range(dim):
                for j in range(dim):
                    if board[k][i][j] == 0:
                        return (k, i, j)

threeInARow = partial(checkGameOver, n=3)
fourInARow = partial(checkGameOver, n=4)
fiveInARow = partial(checkGameOver, n=5)

def defaultTurnChooser(currPlayer):
    '''
    The default turn chooser just alternates between player 0 and player 1.
    '''
    return int(currPlayer == 0)

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--display', help='Print more data', action='store_true')
    args = parser.parse_args()

    display = args.display

    game = BigTicTacToe(DumbAgent(0), DumbAgent(1), Log(0))
    if display:
        game.display()
        time.sleep(2)
    game.play()
    game.reset()
    game.play()
