import flask
from flask import Blueprint
from flask import g

import knotcake.steam
from models import User

def LoginBlueprint(app):
	blueprint = Blueprint("login", __name__)
	
	@blueprint.route("/login")
	def login():
		steamOpenId = knotcake.steam.OpenId()
		steamOpenId.localIdentity = flask.request.url_root
		steamOpenId.returnUrl     = flask.request.url_root + "login"
		
		if "openid.signed" in flask.request.args:
			steamId64 = steamOpenId.validateLogin(flask.request.args)
			if steamId64 is not None:
				steamUser = app.config["SteamWebApi"].getUserBySteamId64(steamId64)
				user = User.registerSteamUser(g.databaseSession, steamUser)
				g.session.logIn(user.id)
				return flask.redirect("/")
		
		return flask.redirect(steamOpenId.generateLoginUrl())
	
	@blueprint.route("/logout")
	def logout():
		g.session.logOut()
		
		return flask.redirect("/")
	
	return blueprint
