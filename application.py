from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
	return "CakeStrap Package Server"

if __name__ == "__main__":
	app.run ()
