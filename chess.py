from utils import Agent, Game, Log
from enum import Enum 
from itertools import permutations
from random import choice 
import copy 

def checkGameOver(board, logger): 
    return False 

def generateInitialState(dim): 
    empty = [[0]*dim for _ in range(dim)]
    for i in range(len(empty)): 
        empty[1][i] = Piece(PieceType.PAWN)
        empty[-2][i] = Piece(PieceType.PAWN)
    
    piecesToPlace = []
    piecesToPlace.append(Piece(PieceType.KING)) 
    piecesToPlace.append(Piece(PieceType.QUEEN))
    for pieceType in [PieceType.BISHOP, PieceType.ROOK, PieceType.KNIGHT]:
        piecesToPlace += [Piece(pieceType), Piece(pieceType)]
    
    placements = list(permutations(piecesToPlace))
    rowOne = choice(placements) 
    rowTwo = choice(placements)
    empty[0] = rowOne
    empty[-1] = rowTwo 
    return empty 

class PieceType(Enum):
    ROOK = "rook"
    KNIGHT = "knight"
    BISHOP = "bishop"
    QUEEN = "queen"
    KING = "king"
    PAWN = "pawn"

class Piece: 
    def __init__(self, type): 
        self.type = type

    def __str__(self): 
        return " " 

    def __repr__(self): 
        return str(self.type)

class Chess(Game): 
    def __init__(self, agentOne, agentTwo, logger): 
        super().__init__(agentOne, agentTwo, logger)
        self.dim = 8 
        self._init_state = generateInitialState(self.dim)
        self._max_turn = float('inf')
        self.board = copy.deepcopy(self._init_state)

    def __str__(self): 
        s = "".join([str(x) + "\n" for x in self.board])
        return s

    def checkGameOver(self): 
        return True 

    def makeMove(self, move): 
        return True 

class DumbAgent(Agent): 
    def getMove(self, board): 
        return (0, 0)

if __name__ == "__main__":
    game = Chess(DumbAgent(0), DumbAgent(1), Log(0))
    game.play()
    game.reset()
    game.play()