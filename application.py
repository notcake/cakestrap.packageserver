import os.path
import time

import flask
from flask import Flask
from flask import g

import sqlalchemy
import sqlalchemy.orm

from session import Session
import knotcake.steam

from models import User

from config import config
app = Flask(__name__)
app.secret_key = "\x1a\x80)^\x0bh\x9e\x82\x0f\"z\xda\x18\xdba1J\xf9\xe1\xb9#S\x1e\xc2L\xc3\xdd'\xab\x02\x05eH<\xb9L\xdd/F\xfb\xe62\xc9\xe6b\xefg\xc2@\xa2\xcaZHWD\xffl\xa2\x18K\x10Y\xe4\xb0"
app.config["DatabaseEngine"] = sqlalchemy.create_engine("mysql://" + config["Database"]["Username"] + ":" + config["Database"]["Password"] + "@" + config["Database"]["Hostname"] + "/" + config["Database"]["DatabaseName"] + "?charset=utf8mb4")
app.config["DatabaseSessionFactory"] = sqlalchemy.orm.sessionmaker(bind = app.config["DatabaseEngine"])
app.config["Path"] = os.path.dirname(os.path.abspath(__file__))
app.config["SteamWebApi"] = knotcake.steam.WebApi(config["SteamApiKey"])

# Blueprints
from jsxblueprint      import JSXBlueprint
from loginblueprint    import LoginBlueprint
from usersblueprint    import UsersBlueprint
from packagesblueprint import PackagesBlueprint
app.register_blueprint(JSXBlueprint(app))
app.register_blueprint(LoginBlueprint(app))
app.register_blueprint(UsersBlueprint(app))
app.register_blueprint(PackagesBlueprint(app))

@app.before_request
def before_request():
	g.session = Session(flask.session)
	g.databaseSession = app.config["DatabaseSessionFactory"] ()
	g.time = time.time()
	g.currentUser = None
	
	if g.session.isLoggedIn():
		g.currentUser = User.getById(g.databaseSession, g.session.userId)
		g.currentUser.lastActivityTimestamp = g.time
	
	g.getJsxFileList = app.blueprints["jsx"].getJsxFileList

@app.teardown_request
def teardown_request(exception):
	databaseSession = getattr(flask.g, "databaseSession", None)
	if databaseSession is not None:
		databaseSession.commit()
        	databaseSession.close()

@app.route("/")
def index():
	session = Session(flask.session)
	
	return flask.render_template("index.html")

if __name__ == "__main__":
	print ("Starting server in debug mode...")
	
	app.debug = True
	app.run (host = "0.0.0.0")
