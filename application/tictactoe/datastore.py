'''
    datastore.py

    Datastore module for the game of Tic-Tac-Toe

    Note: This module currently does nothing. Work to be done to store the state of the game.

'''

class DataStore:

    class State(ndb.Model):
        """   Stores the current state of the board   """
        board = ndb.StringProperty()
        moves = ndb.IntegerProperty()
        date = ndb.DateTimeProperty(auto_now_add=True)

    def retrieveState():
        query = State.query()
        states = query.order(-State.date).fetch(1)
        lastState = []
        turns = None
        # pass the board to play before you can serialize the current state
        if len(states) > 0:
            for state in states:
                lastState = deserializeBoard(state.board)
                turns = state.moves
        else:
            lastState = [['#','#','#'],['#','#','#'],['#','#','#']]
            turns = 9
        return (lastState, turns)

    def storeState():
        serialized_state = serializeBoard(currentState)
        State(board = serialized_state, moves = turns).put()
        return

    def serializeBoard(board):
        state = ""
        for row in board:
            for col in row:
                state += col
        return state

    def deserializeBoard(state):
        ROWS = COLS = 3
        board = []
        count = 0
        while ROWS > 0:
            row = []
            while COLS > 0:
                row.append(str(state[count]))
                count += 1
                COLS -= 1
            board.append(row)
            ROWS -= 1
            COLS = 3
        return board
