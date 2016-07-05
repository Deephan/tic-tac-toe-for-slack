'''
    Notes:

        * Alright, so this is going to the first scrape version of the game.
        * Eventually ill bring in jinja2 for building the template.
        * Next step would be creating the REST layer for slack integration.
        * Then building the interface for slack.

    Done:
        * The initial version is going to be purely console interactive.


    TO DO:
        ** Unit tests
        ** Revamp the architecture (Obviously lacking the expertise, since as an
           architect this should essentially be the first step. But hey, this is
           the start. The end? The day i deploy this app, ill be the pro.)
        ** Migrate the beta project to the main cloud project

    Skeleton:

        Class Game:

            This will be the main class.

            * Members

                (i) Class Board

                        * Members
                            .....

                        * Methods:
                            * Getters
                            * Setters

                (ii) Class Player

                        * Members
                            .....

                        * Methods:
                            * Getters
                            * Setters

                (iii) Score Board

                        * Members
                            .....

                        * Methods:
                            * Getters
                            * Setters

            * Methods:

                (i)   start
                (ii)  play
                (iii) Getters
                        * Status
                        * result
                (iv)  Setters
                        * place


        TEST CASES:

        (i)   Playing the same move twice by the same/different opponent
        (ii)  Incoming challenge while a game is in session
        (iii) Print the status of an ongoing game
        (iv)  Using a non-numeric character to play a move
        (v)   Challenge a non-slack member

'''
from player import Player
from board import Board
import json

class Game:

    def __init__(self):
        '''   Constructor   '''
        self.board = Board()
        self.one = None
        self.two = None
        self.currentTurn = None
        self.nextTurn = None
        self.winner = None
        self.gameComplete = False
        self.firstPlayer = None
        self.secondPlayer = None
        self.noOfMoves = 9
        return

    def __repr__(self):
        '''   Repr string   '''
        return "Game Created"

    def __str__(self):
        '''   Documentation String   '''
        return "This is a python based game of Tic Tac Toe for two players"

    def determineFirstMove(self, challenger, opponent):
        '''   Coin toss to determine which player goes first   '''
        import random
        return challenger if random.random() > 0.5 else opponent

    def getCurrentTurn(self):
        '''   Return which player makes the current move   '''
        return self.currentTurn.getName() + " - (" + self.currentTurn.getMark() + ")"

    def getNextTurn(self):
        '''   Return which player makes the next move   '''
        return self.nextTurn.getName() + " - (" + self.nextTurn.getMark() + ")"

    def getCurrentPlayer(self):
        '''   Return the name of the current player   '''
        return self.currentTurn.getName()

    def setMoves(self, moves):
        '''   Set the number of moves played so far  '''
        self.noOfMoves = moves
        return

    def isGameComplete(self):
        '''   Return the state of the game   '''
        return True if self.gameComplete is True else False

    def evaluate(self):
        '''
            Evaluate the current state of the board for completion of the game.

            A game is complete if any of the three cases apply

            (i)   Any row with only crosses (X) or circles (O)
            (ii)  Any column with only crosses (X) or circles (O)
            (iii) Any diagonal with only crosses (X) or circles (O)

            Note that a cross or circle uniquely identifies a player

         '''
        from pymatrix import matrix
        gameBoard = self.board
        mat = matrix(gameBoard.board)
        players = ['X','O']

        def evaluateRows():
            """   Evaluates each row in the matrix for a win   """
            for sign in players:
                for row in mat.rows():
                    win = True
                    for element in row:
                        if(element != sign):
                            win = False
                    if win is True:
                        self.winner = self.getNextTurn()
                        self.gameComplete = True
                        return
            return

        def evaluateColumns():
            """   Evaluates each row in the matrix for a win   """
            for sign in players:
                for col in mat.cols():
                    win = True
                    for element in col:
                        if(element != sign):
                            win = False
                    if win is True:
                        self.winner = self.getNextTurn()
                        self.gameComplete = True
                        return
            return

        def evaluateDiagonals():
            """   Evaluates each diagonal in the matrix for a win   """
            for sign in players:
                #   Right Diagonal
                if(gameBoard.getElement(1) == gameBoard.getElement(5) == gameBoard.getElement(9) == sign):
                    self.gameComplete = True
                    self.winner = self.getNextTurn()
                    return
                #   Left Diagonal
                if(gameBoard.getElement(3) == gameBoard.getElement(5) == gameBoard.getElement(7) == sign):
                    self.gameComplete = True
                    self.winner = self.getNextTurn()
                    return
            return

        evaluateRows()
        evaluateColumns()
        evaluateDiagonals()
        return

    def declareResult(self):
        """   Declare the winner or the result if its a draw   """
        result = None
        if self.gameComplete is False : result = "Game Drawn!!"
        if self.winner is not None : result = self.winner + " wins!!!"
        print result
        return result

    def play(self, pos, currentBoard, moves, autoplay = False):
        """   Simulate autoplay. Naive Algorithm, No AI applied   """
        import random, sys, json
        state = ""
        print "\n\nPlaying position: ",pos
        if autoplay is True:
            availableMoves = [pos for pos in range(1,10)]
            moves = 9
            firstmove = True
            while moves > 0 and self.gameComplete is False :
                line = None
                random.shuffle(availableMoves)
                pos = availableMoves.pop()
                if firstmove :
                    self.firstPlayer.setPosition(pos)
                    self.board.setCross(pos)
                else :
                    self.secondPlayer.setPosition(pos)
                    self.board.setCircle(pos)
                self.currentTurn = self.firstPlayer if firstmove is True else self.secondPlayer
                self.nextTurn = self.secondPlayer if firstmove is True else self.firstPlayer
                self.board.getState()
                self.evaluate()
                if self.gameComplete is False: print self.getNextTurn()+ " plays next!"
                moves -= 1
                firstmove = not firstmove
            self.nextMove = None
            if moves is 0 : print 'End of Game'
            print "Number of moves made by first player: ", self.firstPlayer.getNoOfMovesPlayed()
            print "Number of moves made by second player: ", self.secondPlayer.getNoOfMovesPlayed()
            self.declareResult()
        else:
            self.noOfMoves = moves
            self.board.setBoard(currentBoard)
            print "\n\nNo of Moves : ", self.noOfMoves
            print '\n\nBefore: \n'
            self.board.getState()
            if self.noOfMoves > 0:
                if self.noOfMoves % 2 != 0:
                    self.board.setCross(int(pos))
                    self.secondPlayer.setPosition(pos)
                else:
                    self.board.setCircle(int(pos))
                    self.firstPlayer.setPosition(pos)
                self.noOfMoves -= 1
                (self.currentTurn, self.nextTurn) = (self.nextTurn, self.currentTurn)
                # Technically this is also the nextTurn player
                print '\n\nAfter: \n'
                self.board.getState()
                self.evaluate()
                print "\n\nBOARD =",self.board.board
            if self.gameComplete is True:
                self.declareResult()
        return self.board.board

    def createPlayers(self, playerOne, playerTwo):
        self.one = Player('X')
        self.two = Player('O')
        self.firstPlayer = self.one
        self.firstPlayer.setName(playerOne)
        self.secondPlayer = self.two
        self.secondPlayer.setName(playerTwo)
        self.currentTurn = self.firstPlayer
        self.nextTurn = self.secondPlayer
        return

    def reset(self):
        self.gameComplete = False
        return

    def isMoveAllowed(self, pos):
        '''   Check to see if the position is allowed   '''
        visited_moves = self.firstPlayer.getPositions()+self.secondPlayer.getPositions()
        return True if pos not in visited_moves else False

    def isMoveValid(self, pos):
        '''   Check to see if the position is valid move   '''
        valid_moves = list("123456789")
        return True if pos in valid_moves else False

    def startNewGame(self, challenger, opponent, autoPlay=False):
        print "Coin toss: Determining the First Player"
        statusMsg = ""
        if self.determineFirstMove(challenger, opponent) is challenger:
            print challenger," goes first"
            self.createPlayers(challenger, opponent)
        else:
            print opponent," goes first"
            self.createPlayers(opponent, challenger)
        statusMsg += self.getCurrentTurn() + " goes first, "
        statusMsg += self.getNextTurn() +  " goes next!"
        if autoPlay is True:
            # firstplayer, secondplayer will be removed. Its just for the case of autoplay
            blankBoard = [['#','#','#'],['#','#','#'],['#','#','#']]
            self.play(0,blankBoard,9,True)
        else:
            print "Game Created"
        return statusMsg



#g = Game()
#g.startNewGame("Challenger", "Opponent", True)
