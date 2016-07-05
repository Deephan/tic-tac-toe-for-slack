'''
    player.py

    Player module for the game of Tic-Tac-Toe

'''

class Player:

    def __init__(self, sign):
        """   Constructor   """
        self.positions = []
        self.mark = sign
        self.name = None
        return

    def __str__(self):
        """   Documentation String   """
        return "Player of Tic-Tac-Toe"

    def getMark(self):
        """   Return the mark of the player   """
        return self.mark

    def getName(self):
        """   Return the username of the player   """
        return self.name

    def getNoOfMovesPlayed(self):
        """   Return the number of moves played by this player   """
        return len(self.positions)

    def getPositions(self):
        """   Return the list of positions played by the player   """
        return self.positions

    def setPosition(self, pos):
        """   Set the move for this player   """
        self.positions.append(pos)
        return

    def setName(self, username):
        """   Set the username for this player   """
        self.name = username
        return
