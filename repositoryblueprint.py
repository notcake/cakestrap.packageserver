import json

import flask
from flask import Blueprint
from flask import g

import api
from models import User, Package, DirectoryTree

def RepositoryBlueprint(app):
	blueprint = Blueprint("repository", __name__)
	
	@blueprint.route("/repository.json", defaults = { "type": "json" })
	@api.json()
	def repository(type):
		return {
			"name":        app.config["Repository"]["Name"],
			"description": app.config["Repository"]["Description"],
			"releases":    flask.url_for("packagereleases.packageReleases", type = "json")
		}
	
	return blueprint
