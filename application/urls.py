from application import app
from flask import request
from flask import json
from flask import jsonify
from google.appengine.ext import ndb
from application.tictactoe.game import Game
from application.tictactoe.player import Player
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

'''
    TEST CASES:

    (i)    /tictactoe-help
    (ii)   Display the state of the board publicly on the channel
    (iii)  User authentication using user_id
    (iv)   Status also displays "your move"
    (v)    Winner status message shouldn't display the next move

'''
resp = ""
slackResponse={}
currentGame = None
serialized_state = None
challenger = None
opponent = None

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


@app.route('/tictactoe')
def play():
    """   Return all the possible slash commands required to play the game   """
    help_text = "You have the following options: \n\n - /tictactoe challenge @user (To challenge @user for a game)"
    return help_text

@app.route('/tictactoe-accept', methods = ['POST'])
def accept():
    """   Accept the Tic-Tac-Toe Challenge   """
    global currentGame, serialized_state, resp, slackResponse
    obj = {"response_type": "ephemeral"}
    status = None
    challenger = None
    opponent = None
    if slackResponse is not None:
        challenger = "@"+slackResponse['user_name']
        opponent = None if slackResponse['text'] is "" else slackResponse['text']
    resp = request.form
    response_str="%s" % resp
    lst = []
    for st in response_str[20:-2].split(","):
        lst.append(st.replace("(","").replace(")","").replace("u'","").replace("'","").lstrip())
    Response = {lst[i]:lst[i+1] for i in range(0, len(lst), 2)}
    username = '@' + Response['user_name']
    if currentGame is None and challenger is not None and opponent is not None:
        serialized_state = "#########" # Initial state of the game. Is this needed?
        currentGame = Game()
        if username == opponent :
            accept_txt = opponent + " has accepted " + challenger + "'s challenge!\n\nDetermine who goes first by a coin toss..\n\n"
            status = currentGame.startNewGame(challenger, opponent)
            status = accept_txt + status
            obj["response_type"] = "in_channel"
    elif currentGame is not None and challenger is not None and opponent is not None:
        status = "Game in progress...\n\n"
        status += "You can either choose to \n\n\t"
        status += "(a) Use /tictactoe-status to get the status of the game\n\n\t"
        status += "(b) Challenge an opponent after the current game completes.\n\nSlack /tictactoe-help for more details."
    else :
        status = "Invalid Command..\n\nChallenge a slack user to start a new game.\n\n/tictactoe-challenge @user\n\n@user has to be on Slack!"
    obj["text"] = status
    return jsonify(obj)

@app.route('/tictactoe-reject', methods = ['POST'])
def reject():
    """   Reject the Tic-Tac-Toe Challenge  """
    global currentGame, resp, slackResponse
    status = None
    obj = {"response_type": "ephemeral"}
    resp = request.form
    response_str="%s" % resp
    lst = []
    challenger = None
    opponent = None
    if slackResponse is not None:
        challenger = "@"+slackResponse['user_name']
        opponent = None if slackResponse['text'] is "" else slackResponse['text']
    for st in response_str[20:-2].split(","):
        lst.append(st.replace("(","").replace(")","").replace("u'","").replace("'","").lstrip())
    Response = {lst[i]:lst[i+1] for i in range(0, len(lst), 2)}
    username = '@' + Response['user_name']
    if currentGame is not None and challenger is not None and opponent is not None:
        status = "Game in progress...\n\n"
        status += "You can either choose to \n\n\t"
        status += "(a) Use /tictactoe-status to get the status of the game\n\n\t"
        status += "(b) Challenge an opponent after the current game completes.\n\nSlack /tictactoe-help for more details."
    elif currentGame is None and challenger is not None and opponent is not None:
        if opponent == username:
            status = opponent + " has rejected " + challenger + "'s challenger request!\n\nFloor is open for a new challenge!'"
        reset()
        obj["response_type"] = "in_channel"
    else:
        status = "Invalid Command..\n\nChallenge a slack user to start a new game.\n\n/tictactoe-challenge @user\n\n@user has to be on Slack!"
    obj["text"] = status
    return jsonify(obj)

@app.route('/tictactoe-challenge', methods = ['POST'])
def api_message():
    global resp, slackResponse, currentGame, serialized_state, challenger, opponent
    status = None
    obj = {"response_type": "ephemeral"}
    if currentGame is None:
        resp = request.form
        response_str="%s" % resp
        lst = []
        for st in response_str[20:-2].split(","):
            lst.append(st.replace("(","").replace(")","").replace("u'","").replace("'","").lstrip())
        slackResponse = {lst[i]:lst[i+1] for i in range(0, len(lst), 2)}
        challenger = "@"+slackResponse['user_name']
        opponent = None if slackResponse['text'] is "" else slackResponse['text']
        if opponent is not None and challenger is not None:
            obj["response_type"] = "in_channel"
            status = challenger +" has challenged "+ opponent + " to a game of Tic-Tac-Toe!\n\n " + opponent + "'s decision pending..."
            #serialized_state = "#########" # Initial state of the game. Is this needed?
            #currentGame = Game()
            #status = currentGame.startNewGame(challenger, opponent)
        else:
            status = "Challenge a slack user to start a new game.\n\n/tictactoe-challenge @user\n\n@user has to be on Slack!"
    else :
        status = "Game in progress...\n\n"
        status += "You can either choose to \n\n\t"
        status += "(a) Use /tictactoe-status to get the status of the game\n\n\t"
        status += "(b) Challenge an opponent after the current game completes.\n\nSlack /tictactoe-help for more details."
    obj["text"] = status
    return jsonify(obj)

# TO DO: merge routes
@app.route('/tictactoe-play', methods = ['POST'])
def place():
    global resp, slackResponse, currentGame, serialized_state
    return_msg = "Not sure what the problem is.. Check the code."
    obj = {"response_type": "in_channel","text": return_msg}
    if currentGame is not None and currentGame.isGameComplete() is not True:
        response_str = "%s" % str(request.form)
        lst = []
        print response_str
        for st in response_str[20:-2].split(", "):
            lst.append(st.replace("(","").replace(")","").replace("u'","").replace("'","").lstrip())
        slackResponse = {lst[i]:lst[i+1] for i in range(0, len(lst), 2)}
        username = '@'+slackResponse['user_name']
        position = slackResponse['text']
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
        if username == currentGame.getCurrentPlayer(): # BUG: Replacing == with "is" doesn't work
            if not currentGame.isMoveValid(position) :
                obj["response_type"] = "ephemeral"
                return_msg = "Please make a valid move..\n\n/tictactoe-play position\n\nposition can be from 1 to 9\n\n"
            elif not currentGame.isMoveAllowed(position) :
                obj["response_type"] = "ephemeral"
                return_msg = "This position has been played already..\n\n/tictactoe-status to see the current state of the game\n\nPlease make a move that is allowed\n\n"
            else:
                currentState = currentGame.play(position, lastState, turns)
                turns -= 1
                serialized_state = serializeBoard(currentState)
                State(board = serialized_state, moves = turns).put()
                return_msg = getStatus(False)
                if currentGame.isGameComplete() is True or turns == 0:
                    return_msg += "\n\n"+currentGame.declareResult()
                    reset()
        else : # Its not current user's turn
            obj["response_type"] = "ephemeral"
            return_msg = "This turn belongs to " + currentGame.getCurrentTurn()+ "!"
    else :
        obj["response_type"] = "ephemeral"
        return_msg = "Sorry, no moves allowed!\n\nChallenge an opponent to start a new game!\n\nSlack /tictactoe-help for more details."
    obj["text"] = "%s" % return_msg
    return jsonify(obj)

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

@app.route('/tictactoe-status', methods = ['POST'])
def getStatus(returnjson=True):
    """   Returns the current status of the board and also the next player to make the move   """
    global currentGame, serialized_state, challenger, opponent
    status = None
    obj = {"response_type": "in_channel" if returnjson is False else "ephemeral"}
    if currentGame is not None and serialized_state is not None:
        status = "Current State of the game\n\n\n\t\t\t "
        status += currentGame.getCurrentTurn() + "\t plays \t"+ currentGame.getNextTurn() + "\n\n\n\t\t\t\t\t\t"
        status += "========= \n\t\t\t\t\t\t |  {}  |  {}  |  {}  |\n\t\t\t\t\t\t"
        status += " =========\n\t\t\t\t\t\t|  {}  |  {}  |  {}  |\n\t\t\t\t\t\t"
        status += " =========\n\t\t\t\t\t\t|  {}  |  {}  |  {}  |\n\t\t\t\t\t\t =========\n\n\n\n"
        status = status.format(*serialized_state)
        status += "\t\t\t%s makes the next move!"
        # This is a BUG!
        # This might be counter intuitive, but status is called after play
        # When play had already been called the next and current players have already been swapped
        #status = {"text": "Here is a sample text","attachments": [{"text":"Partly cloudy today and tomorrow"}]}
        status = status % currentGame.getCurrentTurn()
    elif currentGame is None and challenger is not None and opponent is not None:
        obj["response_type"] = "ephemeral"
        status = challenger +" has challenged "+ opponent + " to a game of Tic-Tac-Toe!\n\n " + opponent + "'s decision pending..."
        obj["text"] = status
    else :
        obj["response_type"] = "ephemeral"
        status = "No games in progress..\n\nChallenge an opponent to start a new game!\n\nSlack /tictactoe-help for more details."
    obj["text"] = status
    json_response = jsonify(obj)
    return json_response if returnjson is True else status

@app.route('/tictactoe-help', methods = ['POST'])
def help():
    """   Return the help documentation string for the game   """
    doc_str = "\n\n\t\t\tFormat of the Board for Tic-Tac-Toe \n\n\n\t\t\t\t\t\t"
    doc_str += " =========\n\t\t\t\t\t\t|  1  |  2  |  3  |\n\t\t\t\t\t\t"
    doc_str += " =========\n\t\t\t\t\t\t|  4  |  5  |  6  |\n\t\t\t\t\t\t"
    doc_str += " =========\n\t\t\t\t\t\t|  7  |  8  |  9  |\n\t\t\t\t\t\t"
    doc_str += " =========\n\n\n"
    doc_str += "* Each number denotes the positions on the Tic-Tac-Toe Board\n\n"
    doc_str += "* Players alternate placing X's and O's on the Board\n\n"
    doc_str += "* Placing three of a player marks in a horizontal, vertical, or diagonal row wins the game\n\n"
    doc_str += "Game Commands:\n\n\t\t\t(i)    /tictactoe-challenge @user (To challenge @user for a game)\n\n\t\t\t"
    doc_str += "(ii)   /tictactoe-play position (To mark the available position)\n\n\t\t\t"
    doc_str += "(iii)  /tictactoe-status (To get the current status of the game)\n\n\t\t\t"
    doc_str += "(iv)  /tictactoe-accept (To accept the challenge)\n\n\t\t\t"
    doc_str += "(v)   /tictactoe-reject (To reject the challenge)\n\n"
    doc_str = "%s" % doc_str
    return jsonify({"response_type": "in_channel","text": doc_str})


@app.route('/tictactoe-status')
def status():
    """   Returns the current status of the board and also the next player to make the move   """
    global currentGame
    status = "Current State of the game\n\n\n\t\t\t========= \n\t\t\t|  1  |  2  |  3  |\n\t\t\t"
    status += "=========\n\t\t\t|  4  |  5  |  6  |\n\t\t\t"
    status += "=========\n\t\t\t|  7  |  8  |  9  |\n\t\t\t=========\n\n\n\n"
    status += "%s makes the current move"
    return status % currentGame.getCurrentTurn()

@app.route('/ttt')
def chall():
    """   Return all the possible slash commands required to play the game   """
    global slackResponse, resp
    response_str = "%s" % resp
    '''lst = []
    for st in response_str[20:-2].split(","):
        lst.append(st.replace("(","").replace(")","").replace("u'","").replace("'","").lstrip())
    slackResponse = {lst[i]:lst[i+1] for i in range(0, len(lst), 2)}'''
    return "%s" % response_str

@app.route('/currentMove')
def getCurrentMove():
    """   Return all the possible slash commands required to play the game   """
    global currentGame
    return currentGame.getCurrentTurn()

@app.route('/nextMove')
def getNextMove():
    """   Return all the possible slash commands required to play the game   """
    global currentGame
    return currentGame.getNextTurn()

@app.route('/players')
def getPlayers():
    """   Return all the possible slash commands required to play the game   """
    global currentGame, slackResponse
    challenger = "@"+slackResponse['user_name']
    opponent = slackResponse['text']
    (firstPlayer, secondPlayer) = currentGame.determineFirstMove(challenger, opponent)
    return "{0} goes first, {1} goes second".format(firstPlayer, secondPlayer)

@app.route('/tictactoe-reset')
def reset():
    """   Return all the possible slash commands required to play the game   """
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

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
