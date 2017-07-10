from application import app
from flask import request
from flask import json
from flask import jsonify
from google.appengine.ext import ndb
from application.tictactoe.game import Game
from application.tictactoe.player import Player
from application.tictactoe.utils import MessageBuilder
from application.tictactoe.utils import SlackResponseBuilder
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

resp = ""
slackResponse={}
currentGame = None
serialized_state = None
challenger = None
opponent = None
message = MessageBuilder()
srb = SlackResponseBuilder()

# TO DO: Needs to be moved to the datastore module
class State(ndb.Model):
    """   Stores the current state of the board   """
    board = ndb.StringProperty()
    moves = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    resp = "Health check"
    return "Hello World" if resp is True else "%s" % resp

@app.route('/tictactoe-accept', methods = ['POST'])
def accept():
    """   Accept the Tic-Tac-Toe Challenge   """
    global currentGame, serialized_state, resp, slackResponse, message, srb
    obj = {"response_type": "ephemeral"}
    status = None
    challenger = None
    opponent = None
    if slackResponse is not None:
        challenger = "@"+slackResponse['user_name']
        opponent = None if slackResponse['text'] is "" else slackResponse['text']
    Response = srb.getSlackResponse(request.form)
    username = '@' + Response['user_name']
    if currentGame is None and challenger is not None and opponent is not None:
        serialized_state = "#########" # Initial state of the game. Is this needed?
        currentGame = Game()
        if username == opponent :
            accept_txt = message.getMsg("accept").format(opponent, challenger)
            status = currentGame.startNewGame(challenger, opponent)
            status = accept_txt + status
            obj["response_type"] = "in_channel"
    elif currentGame is not None and challenger is not None and opponent is not None:
        status = message.getMsg("ga")
    else :
        status = message.getMsg("iagi")
    obj["text"] = status
    obj["mrkdwn"] = "true"
    return jsonify(obj)

@app.route('/tictactoe-reject', methods = ['POST'])
def reject():
    """   Reject the Tic-Tac-Toe Challenge  """
    global currentGame, resp, slackResponse, message, srb
    status = None
    obj = {"response_type": "ephemeral"}
    challenger = None
    opponent = None
    if slackResponse is not None:
        challenger = "@"+slackResponse['user_name']
        opponent = None if slackResponse['text'] is "" else slackResponse['text']
    Response = srb.getSlackResponse(request.form)
    username = '@' + Response['user_name']
    if currentGame is not None and challenger is not None and opponent is not None:
        status = message.getMsg("ga")
    elif currentGame is None and challenger is not None and opponent is not None:
        if opponent == username:
            status = message.getMsg("reject").format(opponent, challenger)
        reset()
        obj["response_type"] = "in_channel"
    else:
        status = message.getMsg("iagi")
    obj["text"] = status
    return jsonify(obj)

@app.route('/tictactoe-challenge', methods = ['POST'])
def api_message():
    """   Challenge an opponent for a game of Tic-Tac-Toe and return the pending message   """
    global resp, slackResponse, currentGame, serialized_state, challenger, opponent, message, srb
    status = None
    obj = {"response_type": "ephemeral"}
    if currentGame is None and challenger is None and opponent is None:
        slackResponse = srb.getSlackResponse(request.form)
        #  USE CASE: When an user challenges nobody
        opponent = None if slackResponse['text'] is "" else slackResponse['text']
        #  USE CASE: When there is no opponent do not set the challenger
        if opponent is not None : challenger = "@"+slackResponse['user_name']
        #  USE CASE: When there is a challenger and an opponent print the challenge status
        if opponent is not None and challenger is not None:
            obj["response_type"] = "in_channel"
            status = message.getMsg("pending").format(challenger, opponent, opponent)
        else:
        #  USE CASE: When there is no game in progress print the inactive status message for an incoming challenge
            status = message.getMsg("gi")
    else :
        status = message.getMsg("ga")
    obj["text"] = status
    return jsonify(obj)

# TO DO: merge routes
@app.route('/tictactoe-play', methods = ['POST'])
def place():
    """   Place a mark at the specific position and returns who play the next move or game result  """
    global resp, slackResponse, currentGame, serialized_state, message, srb
    return_msg = None
    challenger = None
    opponent = None
    if slackResponse is not None:
        challenger = "@"+slackResponse['user_name']
        opponent = None if slackResponse['text'] is "" else slackResponse['text']
    obj = {"response_type": "ephemeral"}
    if currentGame is not None and currentGame.isGameComplete() is not True:
        slackResponse = srb.getSlackResponse(request.form)
        username = '@'+slackResponse['user_name']
        position = slackResponse['text']
        query = State.query()
        states = query.order(-State.date).fetch(1)
        lastState = []
        turns = None
        # pass the board to play before you can serialize the current state
        if len(states) > 0:
            for state in states:
                lastState = _deserializeBoard(state.board)
                turns = state.moves
        else:
            lastState = [['#','#','#'],['#','#','#'],['#','#','#']]
            turns = 9
        if username == currentGame.getCurrentPlayer(): # BUG: Replacing == with "is" doesn't work
            if not currentGame.isMoveValid(position) :
                return_msg = message.getMsg("im")
            elif not currentGame.isMoveAllowed(position) :
                return_msg = message.getMsg("mna")
            else:
                obj["response_type"] = "in_channel"
                currentState = currentGame.play(position, lastState, turns)
                turns -= 1
                serialized_state = _serializeBoard(currentState)
                State(board = serialized_state, moves = turns).put()
                return_msg = getStatus(False, turns)
        else : # Its not current user's turn
            return_msg = message.getMsg("turn").format(currentGame.getCurrentTurn())
    else :
        if challenger is not None and opponent is not None :
            return_msg = message.getMsg("icga")
        else:
            return_msg = message.getMsg("icgi")
    obj["text"] = "%s" % return_msg
    return jsonify(obj)

@app.route('/tictactoe-status', methods = ['POST'])
def getStatus(returnjson=True, *args):
    """   Returns the current status of the board and also the next player to make the move   """
    global currentGame, serialized_state, challenger, opponent, message
    status = None
    turns = None
    if args: turns = args[0]
    obj = {"response_type": "in_channel" if returnjson is False else "ephemeral"}
    if currentGame is not None and serialized_state is not None:
        status = "Current State of the game\n\n\n\t\t\t "
        status += message.getMsg("vs").format(currentGame.getCurrentTurn(), currentGame.getNextTurn())
        status += message.getMsg("raw")
        status = status.format(*serialized_state)
        # This is a BUG!
        # This might be counter intuitive, but status is called after play
        # When play had already been called the next and current players have already been swapped
        if currentGame.isGameComplete() is True or turns == 0:
            status += message.getMsg("result").format(currentGame.declareResult())
            reset()
        else :
            status += message.getMsg("next").format(currentGame.getCurrentTurn())
    elif currentGame is None and challenger is not None and opponent is not None:
        obj["response_type"] = "ephemeral"
        status = message.getMsg("pending").format(challenger, opponent, opponent)
        obj["text"] = status
    else :
        obj["response_type"] = "ephemeral"
        status = message.getMsg("cgi")
    obj["text"] = status
    json_response = jsonify(obj)
    return json_response if returnjson is True else status

@app.route('/tictactoe-help', methods = ['POST'])
def help():
    """   Return the help documentation string for the game   """
    global message
    doc_str = "%s" % message.getMsg("help")
    return jsonify({"response_type": "in_channel","text": doc_str})

@app.route('/currentMove')
def getCurrentMove():
    """   Return the player who owns the current turn   """
    global currentGame
    return currentGame.getCurrentTurn()

@app.route('/nextMove')
def getNextMove():
    """   Return the player who will own the next turn   """
    global currentGame
    return currentGame.getNextTurn()

# Private methods
def _serializeBoard(board):
    state = ""
    for row in board:
        for col in row:
            state += col
    return state

def _deserializeBoard(state):
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

# This REST call is only for debugging
@app.route('/players')
def getPlayers():
    """   Return the results of the coin toss   """
    global currentGame, slackResponse
    challenger = "@"+slackResponse['user_name']
    opponent = slackResponse['text']
    (firstPlayer, secondPlayer) = currentGame.determineFirstMove(challenger, opponent)
    return "{0} goes first, {1} goes second".format(firstPlayer, secondPlayer)

# This REST call is only for debugging
# Use it with caution!!
@app.route('/tictactoe-reset')
def reset():
    """   Reset the game   """
    global currentGame, serialized_state, challenger, opponent, slackResponse
    print request.data
    ndb.delete_multi(State.query().fetch(keys_only=True))
    if currentGame is not None:
        currentGame.winner = None
        currentGame.gameComplete = False
        currentGame = None
    challenger = None
    opponent = None
    slackResponse = None
    if serialized_state is not None: serialized_state = None
    return "Game States cleared" # This is to be modified with an accept/reject attachment

# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
