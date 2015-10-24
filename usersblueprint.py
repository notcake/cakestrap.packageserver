import json

import flask
from flask import Blueprint
from flask import g

import api
from models import User

def UsersBlueprint(app):
	blueprint = Blueprint("users", __name__)
	
	@blueprint.route("/users/<int:steamId64>")
	def user(steamId64):
		return flask.render_template("users/user.html", steamId64 = steamId64)
	
	@blueprint.route("/users/all")
	def all():
		return flask.render_template("users/all.html")
	
	@blueprint.route("/users/<int:steamId64>.json",  defaults = { "type": "json"  })
	@blueprint.route("/users/<int:steamId64>.jsonp", defaults = { "type": "jsonp" })
	@blueprint.route("/users/<int:steamId64>/user.json",  defaults = { "type": "json"  })
	@blueprint.route("/users/<int:steamId64>/user.jsonp", defaults = { "type": "jsonp" })
	@api.json()
	@api.jsonp("var user = new User({});")
	@api.map("toDictionary")
	def userJson(steamId64, type):
		return User.getBySteamId64(g.databaseSession, steamId64)
	
	@blueprint.route("/users/current.json",  defaults = { "type": "json"  })
	@blueprint.route("/users/current.jsonp", defaults = { "type": "jsonp" })
	@api.json()
	@api.jsonp("var currentUser = new User({});")
	@api.map("toDictionary")
	def currentUserJson(type):
		return g.currentUser
	
	@blueprint.route("/users.json",  defaults = { "type": "json"  })
	@blueprint.route("/users.jsonp", defaults = { "type": "jsonp" })
	@blueprint.route("/users/all.json",  defaults = { "type": "json"  })
	@blueprint.route("/users/all.jsonp", defaults = { "type": "jsonp" })
	@api.json()
	@api.jsonp("var users = {}.map(User.create);")
	@api.mapArray("toDictionary")
	def allJson(type):
		return User.getAll(g.databaseSession)
	
	return blueprint
