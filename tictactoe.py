import copy
from utils import Log, Game, Agent

def checkGameOver(board, logger): 
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
        return True, diagOneStarting
    
    if diagTwo and diagTwoStarting!= 0: 
        logger.d(f"Diag Two")
        return True, diagTwoStarting

    return False, 0 

class TicTacToe(Game): 
    def __init__(self, agentOne, agentTwo, logger):
        super().__init__(agentOne, agentTwo, logger) 

        self._init_state =  [[0]*3 for _ in range(3)]
        # self._max_turn = 9
        self.dim = 3 
        self.board = copy.deepcopy(self._init_state)
    
    def __str__(self):
        return "".join([f"{x[0]} {x[1]} {x[2]}" + "\n" for x in self.board])

    def makeMove(self, action):
        # Assumes the move is valid
        pieceToPlay = 1 if self.currPlayer == 0 else 2
        self.board[action[0]][action[1]] = pieceToPlay
        return True

    def checkGameOver(self):
        checkGameOver(self.board, self.logger)

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
    def getMove(self, board): 
        for i in range(self.dim):
            for j in range(self.dim):
                if board[i][j] == 0:
                    return (i, j)

if __name__ == "__main__":
    game = TicTacToe(DumbAgent(0), DumbAgent(1), Log(0))
    game.play()
    game.reset()
    game.play()
