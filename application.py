import flask
from flask import Flask

from session import Session

app = Flask(__name__)

# Blueprints
from loginblueprint import blueprint as loginBlueprint
app.register_blueprint(loginBlueprint)

@app.route("/")
def index():
	session = Session(flask.session)
	
	return flask.render_template("index.html")

if __name__ == "__main__":
	print ("Starting server in debug mode...")
	
	app.debug = True
	app.run (host = "0.0.0.0")
