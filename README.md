# tic-tac-toe-for-slack

This project is created from the google's  [appengine-flask-skeleteon](https://github.com/GoogleCloudPlatform/appengine-flask-skeleton#python-flask-skeleton-for-google-app-engine) as the game is hosted on google cloud.

To execute the project follow the same instructions on the link above. Please be cautioned as the game may not execute properly as the datastore is on the google cloud and it may require appropriate login credentials for the game to execute.

The deployed version of the application is active on google cloud and the url is not exposed here for security reasons. Slack has been integrated with the deployed application's web url for internally executing the slash commands.

![alt text] (https://github.com/Deephan/tic-tac-toe-for-slack/blob/master/Slack-TicTacToe-Help.png "Slack-TicTacToe commands")

Please note that it may be possible execute the game locally as long as the same [slack commands](https://api.slack.com/slash-commands) are registered with the proper action url and if slack can communicate with the locally hosted web application. 

The game can still be execute stand-alone **without** starting the web application by running it as local python program.
To do this navigate to application/tictactoe in your local installation and run the game locally



`python game.py`

Note: Uncomment the last two lines of **game.py** to run the game in autoplay mode. You can also run it manually by passing `autoplay=False` in the argument


`g.startNewGame("Challenger", "Opponent", False)`

The execution of the game would require you to make **POST** calls to the endpoint **/tictactoe-play**. Please note that manually execution is only for debugging purposes and may not be ideally suited for playing the game. The game works best on slack. 

See screenshots: 

https://github.com/Deephan/tic-tac-toe-for-slack/blob/master/Slack-commands-in-action.png
https://github.com/Deephan/tic-tac-toe-for-slack/blob/master/Slack-game-result.png


