'''
    board.py

    Board module for the game of Tic-Tac-Toe

'''
import pprint
import math

class Board:

    def __init__(self):
        """   Constructor   """

        #  \# Signifies empty positions on the board
        self.board = [
            ['#','#','#'],
            ['#','#','#'],
            ['#','#','#']
        ]
        self.rows = 3
        self.cols = 3
        return

    def __str__(self):
        """   Documentation String   """
        doc_str = """

            Board for Tic-Tac-Toe \n
            Board Format:          \n\n
                         =================
                        |  1  |  2  |  3  |
                         =================
                        |  4  |  5  |  6  |
                         =================
                        |  7  |  8  |  9  |
                         =================

        * Each number denotes the positions on the Tic-Tac-Toe Board

        """
        return doc_str

    def getState(self):
        """   Print the current the state of the board   """
        pp = pprint.PrettyPrinter(indent=4)
        for list in self.board:
            pp.pprint(list)
        return

    def getElement(self,position):
        """   Returns the element at the position of the board """
        row = (position / self.rows) - 1 if (position % self.rows) == 0 else (position / self.rows)
        col = (self.cols - 1) if (position % self.rows) == 0 else (position % self.rows) - 1
        return self.board[row][col]

    def setCross(self, position):
        """   Sets a cross at the designated position on the Board   """
        row = (position / self.rows) - 1 if (position % self.rows) == 0 else (position / self.rows)
        col = (self.cols - 1) if (position % self.rows) == 0 else (position % self.rows) - 1
        self.board[row][col] = 'X'
        return

    def setCircle(self, position):
        """   Sets a circle at the designated position on the Board   """
        row = (position / self.rows) - 1 if (position % self.rows) == 0 else (position / self.rows)
        col = (self.cols - 1) if (position % self.rows) == 0 else (position % self.rows) - 1
        self.board[row][col] = 'O'
        return

    def setBoard(self, currBoard):
        self.board = currBoard
        return
