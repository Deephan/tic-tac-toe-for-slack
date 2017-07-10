# tic-tac-toe-for-slack

This project is created from google's  [appengine-flask-skeleteon](https://github.com/GoogleCloudPlatform/appengine-flask-skeleton#python-flask-skeleton-for-google-app-engine) as the game is hosted on google cloud.

To execute the project follow the same instructions on the link above. Please be cautioned as the game may not execute properly unless the appropriate login credentials are provided and since the datastore is on the google cloud.

The deployed version of the application is active on google cloud and the url is not exposed here for security reasons. Slack has been integrated with the deployed application's web url for internally executing the slash commands.

To play the game within slack join the team **deephanmohan85test0.slack.com** and you can play the game in the **#tic-tac-toe** channel.
If you are unable to join the team kindly reach out to me. I can send you an invite as long as the team is actively moderated by slack. 

#### Game commands for Tic-Tac-Toe (Slack /tictactoe-help when you are on the appropriate team)

![alt text] (https://github.com/Deephan/tic-tac-toe-for-slack/blob/master/Slack-TicTacToe-Help.png "Slack-TicTacToe commands")

Please note that it may be possible execute the game locally as long as the same [slack commands](https://api.slack.com/slash-commands) are registered with the proper action url and if slack can communicate with the locally hosted web application. 

The game can still be executed stand-alone **without** starting the web application by running it as local python program.
To do this navigate to **_application/tictactoe_** in your local installation and run the game locally



`python game.py`

Note: Uncomment the last two lines of **game.py** to run the game in autoplay mode. You can also run it manually by passing `autoplay=False` in the argument


`g.startNewGame("Challenger", "Opponent", False)`

The execution of the game would require you to make **POST** calls to the endpoint **/tictactoe-play**. Please note that manually execution is only for debugging purposes and may not be ideally suited for playing the game. The game works best on slack. 

See screenshots: 

https://github.com/Deephan/tic-tac-toe-for-slack/blob/master/Slack-commands-in-action.png
https://github.com/Deephan/tic-tac-toe-for-slack/blob/master/Slack-Game-Result.png


