from flask import Flask
from Scripts.isAuthorised import isAuthorised
from database import DataBaseHandler
from Blueprints.pages import pages
from Blueprints.auth import auth
#creation of webapp and registering all blueprints
app = Flask(__name__)
app.register_blueprint(pages)
app.register_blueprint(auth)
#database and adition of a table
db = DataBaseHandler()
db.createTable()
#allows for me to debug when needed
app.run(debug = True)