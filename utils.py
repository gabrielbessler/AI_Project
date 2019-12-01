from abc import ABC, abstractmethod
import copy 

class Agent(ABC): 
    def __init__(self, playerNum): 
        self.playerNum = playerNum 

    @abstractmethod
    def getMove(self, board): 
        pass 

class Game(ABC):
    def __init__(self, agentOne, agentTwo, logger, turnChooser): 
        self.currPlayer = 0
        self.currTurn = 0
        self.agentOne = agentOne 
        self.agentTwo = agentTwo
        self.logger = logger
        self.turnChooser = turnChooser

    def reset(self): 
        self.logger.e("Resetting...")
        self.currPlayer = 0
        self.currTurn = 0
        self.reset_board()

    @abstractmethod
    def reset_board(self): 
        pass 

    def play(self):
        print("Starting game...")
        while not self.checkGameOver() and self.currTurn != self._max_turn:
            self.logger.e(self)
            if self.currPlayer == 0:
                move = self.agentOne.getMove(self.board, self)
            else: 
                move = self.agentTwo.getMove(self.board, self)
            print(f"move: {str(move)} for player {self.currPlayer}")
            isValid = self.makeMove(move)

            # Update the current player: 
            self.currPlayer = self.turnChooser(self.currPlayer)

            if not isValid: 
                self.logger.f("not a valid move")
            self.currTurn += 1
        print("Game Ended!")
        self.logger.e(self)
        gameResults = self.checkGameOver()
        self.logger.d(gameResults)
        return gameResults
    
    @abstractmethod
    def makeMove(self): 
        pass 

    @abstractmethod
    def checkGameOver(self): 
        pass 

    @abstractmethod
    def getAllActions(self): 
        pass 

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