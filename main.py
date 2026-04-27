from flask import Flask
from database import DataBaseHandler
from Blueprints.pages import pages
from Blueprints.auth import auth
from Blueprints.tournaments import tournaments
#creation of webapp 
app = Flask(__name__)
#secret key is set beforehand so session will work (will be made a better secret key in the future)
app.secret_key = 'thisisabadsecret'
#registering all blueprints
app.register_blueprint(pages)
app.register_blueprint(auth)
app.register_blueprint(tournaments)
#database and addition of a table
db = DataBaseHandler()
db.createTable()
#allows for me to debug when needed
app.run(debug = True)