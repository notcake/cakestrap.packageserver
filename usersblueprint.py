import json

import flask
from flask import Blueprint
from flask import g

from models import User

def UsersBlueprint(app):
	blueprint = Blueprint("users", __name__)
	
	@blueprint.route("/users/<int:steamId64>")
	def user(steamId64):
		return flask.render_template("users/user.html", steamId64 = steamId64)
	
	@blueprint.route("/users/all")
	def all():
		return flask.render_template("users/all.html")
	
	@blueprint.route("/users/<int:steamId64>.json")
	def user_json(steamId64):
		user = User.getBySteamId64(g.databaseSession, steamId64)
		if user is not None: user = user.toDictionary()
		return app.response_class(json.dumps(user), mimetype = "application/json")
	
	@blueprint.route("/users/<int:steamId64>.jsonp")
	def user_jsonp(steamId64):
		user = User.getBySteamId64(g.databaseSession, steamId64)
		if user is not None: user = user.toDictionary()
		return app.response_class("var user = new User(" + json.dumps(user) + ");", mimetype = "application/json")
	
	@blueprint.route("/users/current.json")
	def current_user_json():
		user = g.currentUser
		if user is not None: user = user.toDictionary()
		return app.response_class(json.dumps(user), mimetype = "application/json")
	
	@blueprint.route("/users/current.jsonp")
	def current_user_jsonp():
		user = g.currentUser
		if user is not None: user = user.toDictionary()
		return app.response_class("var currentUser = new User(" + json.dumps(user) + ");", mimetype = "application/json")
	
	@blueprint.route("/users/all.json")
	def all_json():
		users = User.getAll(g.databaseSession)
		users = [ user.toDictionary() for user in users ]
		return app.response_class(json.dumps(users), mimetype = "application/json")
	
	@blueprint.route("/users/all.jsonp")
	def all_jsonp():
		users = User.getAll(g.databaseSession)
		users = [ user.toDictionary() for user in users ]
		return app.response_class("var users = " + json.dumps(users) + ".map(User.Create);", mimetype = "application/json")
	
	return blueprint
