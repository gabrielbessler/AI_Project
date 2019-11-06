import copy
import torch

class Log:
    def __init__(self, output):
        self.output = output

    def log(self, s):
        if self.output:
            print(s) 
        else: 
            pass

class Game: 
    def __init__(self, agentOne, agentTwo, logger):
        self.__init_state =  [[0]*3 for _ in range(3)]
        
        self.dim = 3 
        self.board = copy.deepcopy(self.__init_state)
        self.currPlayer = 0
        self.currTurn = 0
        self.agentOne = agentOne 
        self.agentTwo = agentTwo
        self.logger = logger
    
    def __str__(self):
        s = "".join([f"{x[0]} {x[1]} {x[2]}" + "\n" for x in self.board])
        return s

    def reset(self): 
        self.logger.log("Resetting...")
        self.currPlayer = 0
        self.currTurn = 0
        self.board = copy.deepcopy(self.__init_state)

    def checkGameOver(self): 
        for i in range(self.dim):
            inARow_V = True
            inARow_H = True
            startingPiece_V = self.board[i][0]
            startingPiece_H = self.board[0][i]
            for j in range(1, self.dim):
                if inARow_V and self.board[i][j] != startingPiece_V:
                    inARow_V = False
                if inARow_H and self.board[j][i] != startingPiece_H:
                    inARow_H = False
                    break 
                
            if inARow_V and startingPiece_V != 0:
                return True, startingPiece_V

            if inARow_H and startingPiece_H != 0:
                return True, startingPiece_H
        
        diagOne = True
        diagTwo = True
        diagOneStarting = self.board[0][0]
        diagTwoStarting = self.board[self.dim-1][self.dim-1]
        for i in range(1, self.dim):
            if diagOne and self.board[i][i] != diagOneStarting:
                diagOne = False
            if diagTwo and self.board[self.dim-1-i][self.dim-1-i] != diagTwoStarting:
                diagTwo = False

        if diagOne and diagOneStarting!= 0: 
            return True, diagOneStarting
        
        if diagTwo and diagTwoStarting!= 0: 
            return True, diagTwoStarting

        return False, 0 

    def makeMove(self, action):
        # Assumes the move is valid
        pieceToPlay = 1 if self.currPlayer == 0 else 2
        self.board[action[0]][action[1]] = pieceToPlay
        return True

    def play(self):
        while self.checkGameOver() != True and self.currTurn != 9:
            self.logger.log(self)
            if self.currPlayer == 0:
                move = self.agentOne.getMove(self.board)
                self.currPlayer = 1
            else: 
                move = self.agentTwo.getMove(self.board)
                self.currPlayer = 0
            isValid = self.makeMove(move)
            if not isValid: 
                self.logger.log("not a valid move")
            self.currTurn += 1
        self.logger.log(self)
        self.logger.log(self.checkGameOver())

class ConstAgent():
    def __init__(self, playerNum): 
        pass 
    
    def getMove(self, board): 
        return (2, 2)

class Agent(): 
    def __init__(self, playerNum): 
        self.playerNum = playerNum

    def getMove(self, board): 
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    return (i, j)

if __name__ == "__main__":
    game = Game(Agent(0), ConstAgent(1), Log(True))
    game.play()
    game.reset()
    game.play()
