'''

    utils.py

    Utilities module for building the status messages and parsing incoming slack response_str

'''

class MessageBuilder:

    _responses_ = {
        "GAME_ACTIVE"                      : ('Game in progress...\n\n'
                                              'You can either choose to \n\n\t'
                                              '(a) Use /tictactoe-status to get the status of the game\n\n\t'
                                              '(b) Challenge an opponent after the current game completes.\n\n'
                                              'Slack /tictactoe-help for more details.'),

        "GAME_INACTIVE"                    : ('Challenge a slack user to start a new game.\n\n'
                                              '/tictactoe-challenge @user\n\n'
                                              '@user has to be on Slack!'),

        "INVALID_MOVE"                     : ('Please make a valid move..\n\n'
                                              '/tictactoe-play position\n\n'
                                              'position can be from 1 to 9\n\n'),

        "MOVE_NOT_ALLOWED"                 : ('This position has been played already..\n\n'
                                              '/tictactoe-status to see the current state of the game\n\n'
                                              'Please make a move that is allowed\n\n'),

        "INVALID_COMMAND_GAME_ACTIVE"      : ('Invalid Command..\n\n'
                                              'An user has challenged an other user\n\n'
                                              'This command can only be used during an active gameplay'),

        "INVALID_COMMAND_GAME_INACTIVE"    : ('Sorry, no moves allowed!\n\n'
                                              'Challenge an opponent to start a new game!\n\n'
                                              'Slack /tictactoe-help for more details.'),

        "CHALLENGE_GAME_INACTIVE"          : ('No games in progress..\n\n'
                                              'Challenge an opponent to start a new game!\n\n'
                                              'Slack /tictactoe-help for more details.'),

        "INVALID_ACCEPT_GAME_INACTIVE"     : ('Invalid Command..\n\n'
                                              'Challenge a slack user to start a new game.\n\n'
                                              '/tictactoe-challenge @user\n\n'
                                              '@user has to be on Slack!'),

        "HELP"                             : ('\n\n\t\t\tFormat of the Board for Tic-Tac-Toe \n\n\n\t\t\t\t\t\t'
                                              ' =========\n\t\t\t\t\t\t|  1  |  2  |  3  |\n\t\t\t\t\t\t'
                                              ' =========\n\t\t\t\t\t\t|  4  |  5  |  6  |\n\t\t\t\t\t\t'
                                              ' =========\n\t\t\t\t\t\t|  7  |  8  |  9  |\n\t\t\t\t\t\t'
                                              ' =========\n\n\n'
                                              '* Each number denotes the positions on the Tic-Tac-Toe Board\n\n'
                                              '* Players alternate placing X\'s and O\'s on the Board\n\n'
                                              '* Placing three of a player marks in a horizontal, vertical, or diagonal row wins the game\n\n'
                                              'Game Commands:\n\n\t\t\t(i)    /tictactoe-challenge @user (To challenge @user for a game)\n\n\t\t\t'
                                              '(ii)   /tictactoe-play position (To mark the available position)\n\n\t\t\t'
                                              '(iii)  /tictactoe-status (To get the current status of the game)\n\n\t\t\t'
                                              '(iv)  /tictactoe-accept (To accept the challenge)\n\n\t\t\t'
                                              '(v)   /tictactoe-reject (To reject the challenge)\n\n'),

        "RAW_STATE"                        : ('========= \n\t\t\t\t\t\t |  {}  |  {}  |  {}  |\n\t\t\t\t\t\t'
                                              ' =========\n\t\t\t\t\t\t|  {}  |  {}  |  {}  |\n\t\t\t\t\t\t'
                                              '=========\n\t\t\t\t\t\t|  {}  |  {}  |  {}  |\n\t\t\t\t\t\t'
                                              ' =========\n\n\n\n'),

        "VERSUS"                           :  '{} \t plays \t {} \n\n\n\t\t\t\t\t\t',

        "PENDING"                          : ('{} has challenged {} to a game of Tic-Tac-Toe!\n\n'
                                              '{}\'s decision is pending...'),

        "TURN"                             :  'This turn belongs to {}!',

        "NEXT_TURN"                        :  '\t\t\t{} makes the next move!',

        "RESULT"                           :  '\n\n\n\t\t\tGame Result: {}',

        "ACCEPT"                           : ('{} has accepted {}\'s challenge!\n\n'
                                              'Determine who goes first by a coin toss..\n\n'),

        "REJECT"                           : ('{} has rejected {}\'s challenge request!\n\n'
                                              'Floor is open for a new challenge!')
    }

    def getMsg(self, state):
        msg = None
        if state is "ga": msg = self._responses_["GAME_ACTIVE"]
        if state is "gi": msg = self._responses_["GAME_INACTIVE"]
        if state is "im": msg = self._responses_["INVALID_MOVE"]
        if state is "mna": msg = self._responses_["MOVE_NOT_ALLOWED"]
        if state is "icga": msg = self._responses_["INVALID_COMMAND_GAME_ACTIVE"]
        if state is "icgi": msg = self._responses_["INVALID_COMMAND_GAME_INACTIVE"]
        if state is "cgi": msg = self._responses_["CHALLENGE_GAME_INACTIVE"]
        if state is "iagi": msg = self._responses_["INVALID_ACCEPT_GAME_INACTIVE"]
        if state is "help": msg = self._responses_["HELP"]
        if state is "raw": msg = self._responses_["RAW_STATE"]
        if state is "vs" : msg = self._responses_["VERSUS"]
        if state is "pending" : msg = self._responses_["PENDING"]
        if state is "turn" : msg = self._responses_["TURN"]
        if state is "result" : msg = self._responses_["RESULT"]
        if state is "next" : msg = self._responses_["NEXT_TURN"]
        if state is "accept" : msg = self._responses_["ACCEPT"]
        if state is "reject" : msg = self._responses_["REJECT"]
        return msg

class SlackResponseBuilder:

    def getSlackResponse(self, form = None):
        _obj = {}
        response_str = "%s" % form
        lst = []
        for st in response_str[20:-2].split(","):
            lst.append(st.replace("(","").replace(")","").replace("u'","").replace("'","").lstrip())
        _obj = {lst[i]:lst[i+1] for i in range(0, len(lst), 2)}
        return _obj
