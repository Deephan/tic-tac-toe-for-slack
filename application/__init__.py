from flask import Flask
app = Flask("application")
app.config['DEBUG'] = True

import urls
