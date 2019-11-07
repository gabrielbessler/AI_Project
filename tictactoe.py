import copy

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

class Log:
    def __init__(self, output_level):
        # 0 = Everything
        # 1 = Debug 
        # 2 = Fatal Only 
        self.output = output_level

    def e(self, s):
        if self.output <= 0:
            print(s) 

    def d(self, s): 
        if self.output <= 1:
            print(s)

    def f(self, s): 
        if self.output <= 2: 
            print(s)


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
        self.logger.e("Resetting...")
        self.currPlayer = 0
        self.currTurn = 0
        self.board = copy.deepcopy(self.__init_state)


    def makeMove(self, action):
        # Assumes the move is valid
        pieceToPlay = 1 if self.currPlayer == 0 else 2
        self.board[action[0]][action[1]] = pieceToPlay
        return True

    def checkGameOver(self):
        checkGameOver(self.board, self.logger)

    def play(self):
        while self.checkGameOver() != True and self.currTurn != 9:
            self.logger.e(self)
            if self.currPlayer == 0:
                move = self.agentOne.getMove(self.board)
                self.currPlayer = 1
            else: 
                move = self.agentTwo.getMove(self.board)
                self.currPlayer = 0
            isValid = self.makeMove(move)
            if not isValid: 
                self.logger.f("not a valid move")
            self.currTurn += 1
        self.logger.e(self)
        gameResults = self.checkGameOver()
        self.logger.d(gameResults)
        return gameResults 

class ValueAgent():
    def __init__(self, playerNum, valueFunction): 
        self.valueFunction = valueFunction
    
    def getMove(self, board): 
        action = self.valueFunction(board)
        return self.convert(action) 

    def convert(self, action):
        return (action % 3, action // 3)

class DumbAgent(): 
    def __init__(self, playerNum): 
        self.playerNum = playerNum

    def getMove(self, board): 
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    return (i, j)

if __name__ == "__main__":
    game = Game(DumbAgent(0), DumbAgent(1), Log(0))
    game.play()
    game.reset()
    game.play()
